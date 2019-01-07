from odoo import api, fields, models, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    machine_user_id = fields.Char()