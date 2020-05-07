###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import models, fields, api

class AccessGroups(models.Model):
    
    _name = 'muk_security.access_groups'
    _description = "Record Access Groups"
    _inherit = 'muk_utils.mixins.groups'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    perm_read = fields.Boolean(
        string='Quyền đọc')
    
    perm_create = fields.Boolean(
        string='Quyền tạo')
    
    perm_write = fields.Boolean(
        string='Quyền ghi')
    
    perm_unlink = fields.Boolean(
        string='Quyền xóa')
 