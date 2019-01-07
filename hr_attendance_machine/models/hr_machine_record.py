from odoo import api, fields, models, _


class HrMachineRecord(models.Model):
    _name = 'hr.machine.record'
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        pass

    machine_id = fields.Many2one('hr.machine', required=True)
    machine_user_id = fields.Char()
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
        ('2','Type_2'),
        ('3','Password'),
        ('4','Card')
    ])

    timestamp = fields.Datetime()