from . import models

def pre_init_hook(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '13.0': 
        raise Warning('Module for Odoo 13.0, found {}.'.format(server_serie))
    return True