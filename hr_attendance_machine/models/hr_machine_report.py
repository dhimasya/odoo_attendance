# -*- coding: utf-8 -*-
from odoo import tools
from odoo import models, fields, api, _


class HrMachineReport(models.Model):
    _name = 'hr.machine.report'
    _auto = False
    _order = 'timestamp desc'

    date = fields.Datetime(string='Create Date')
    name = fields.Many2one('hr.employee', string='Employee')
    address_id = fields.Many2one('res.partner', string='Working Address')
    type = fields.Selection([
        ('0', 'Check In'),
        ('1', 'Check Out'),
        ('2', 'Break Out'),
        ('3', 'Break In'),
        ('4', 'Overtime In'),
        ('5', 'Overtime Out')
    ])

    method = fields.Selection([
        ('1', 'Finger'),
        ('15', 'Face'),
        ('2', 'Type_2'),
        ('3', 'Password'),
        ('4', 'Card')
    ])
    timestamp = fields.Datetime()

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_machine_report')
        query = """
            CREATE OR REPLACE VIEW hr_machine_report AS (
                SELECT
                    min(id) as id,
                    employee_id as name,
                    write_date as date,
                    address_id,
                    method,
                    timestamp,
                    type
                FROM hr_machine_record
                GROUP BY
                    employee_id,
                    write_date,
                    address_id,
                    method,
                    type,
                    timestamp
            )
        """
        self._cr.execute(query)


