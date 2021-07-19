from odoo import api, fields, models, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    machine_user_id = fields.Char()

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        pass