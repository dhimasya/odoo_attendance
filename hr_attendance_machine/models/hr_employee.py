from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    machine_user_id = fields.Char()