from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import _tz_get
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as SDTF
from zk import ZK, const
from datetime import datetime
import pytz
import logging

_logger = logging.getLogger(__name__)

class HrMachine(models.Model):
    _name = 'hr.machine'
    
    name = fields.Char(string='IP', required=True)
    port = fields.Integer(required=True)
    timezone = fields.Selection(_tz_get, required=True)
    address_id = fields.Many2one('res.partner', string='Working Address')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)


    def connect(self):
        device = ZK(self.name, port=self.port, timeout=60, password=0, force_udp=False, ommit_ping=False)
        return device.connect()

    # @api.multi
    def test_connection(self):
        for machine in self:
            conn = False
            try:
                conn = machine.connect()
            except Exception as e:
                raise ValidationError("Process terminate : {}".format(e))
            if conn:
                conn.disconnect()
                raise ValidationError(_("device connection test success!"))
            else:
                raise UserError(_("device connection test failed!"))
    
    # @api.multi
    def clear_attendance(self):
        for machine in self:
            conn = False
            try:
                conn = machine.connect()
                if conn:
                    conn.disable_device()
                    conn.clear_attendance()
                    self._cr.execute("""DELETE FROM hr_machine_record WHERE machine_id = %s""" % (machine.id))
                    conn.enable_device()
                else:
                    raise UserError(_("Unable to connect, please check the parameters and network connections."))
            except Exception as e:
                raise ValidationError("Process terminate : {}".format(e))
            finally:
                if conn:
                    conn.disconnect()

    @api.model
    def scheduled_download_attendance(self):
        machines = self.env['hr.machine'].search([])
        for machine in machines:
            _logger.info('scheduled download attendance for %s:%s started' % (machine.name, machine.port))
            machine.download_attendance()
            

    # @api.multi
    def download_attendance(self):
        MachineRecord = self.env['hr.machine.record']
        HrAttendance = self.env['hr.attendance']
        employees = self.env['hr.employee'].search([('machine_user_id', '!=', False)])
        for machine in self:
            machine_tz = pytz.timezone(machine.timezone)
            conn = False
            try:
                conn = machine.connect()
            except Exception as e:
                raise ValidationError("Process terminate : {}".format(e))
            if conn:
                conn.disable_device()
                attendances = conn.get_attendance()
                conn.disconnect()
                for employee in employees:
                    previous_record = MachineRecord.search([('machine_user_id', '=', employee.machine_user_id)], order="timestamp desc", limit=1)
                    if previous_record:
                        previous_timestamp = previous_record.timestamp.astimezone(machine_tz)
                        employee_attendances = list(filter(lambda r: r.user_id == employee.machine_user_id and machine_tz.localize(r.timestamp) > previous_timestamp, attendances))
                    else:
                        employee_attendances = list(filter(lambda r: r.user_id == employee.machine_user_id, attendances))
                    for row in employee_attendances:
                        timestamp = machine_tz.localize(row.timestamp)
                        timestamp_utc = timestamp.astimezone(pytz.utc)
                        MachineRecord.create({
                            'employee_id': employee.id,
                            'machine_id': machine.id,
                            'machine_user_id': row.user_id,
                            'type': str(row.punch),
                            'method': str(row.status),
                            'timestamp': timestamp_utc,
                            'address_id': machine.address_id.id,
                        })
                        open_attendance = HrAttendance.search([
                            ('employee_id', '=', employee.id),
                            ('check_out', '=', False)
                        ], limit=1, order="check_in desc")
                        if row.punch == 0: #check-in 
                            if not open_attendance:
                                # last_attendance = HrAttendance.search([
                                #     ('employee_id', '=', employee.id),
                                # ], limit=1, order="check_in desc")
                                # if last_attendance.check_in.date() != timestamp_utc.date():
                                HrAttendance.create({
                                    'employee_id': employee.id,
                                    'check_in': timestamp_utc
                                })
                        if row.punch == 1: #check-out
                            open_attendance.write({
                                'check_out': timestamp_utc
                            })
            else:
                raise UserError(_("Unable to get the attendance log."))
