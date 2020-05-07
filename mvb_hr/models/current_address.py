from odoo import api, fields, models, _

class CurrentAddress(models.Model):
    _name = 'current.address'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char(compute='_compute_address', store="True")
    current_address = fields.Char('Số/Đường')
    current_ward_id = fields.Many2one(
        "res.country.state.district.ward",
        "Phường/Xã",
        domain="[('district_id', '=', current_district_id)]")
    current_district_id = fields.Many2one(
        "res.country.state.district",
        "Quận/Huyện",
        domain="[('state_id', '=', current_state_id)]")
    current_state_id = fields.Many2one(
        "res.country.state",
        "Tỉnh/Thành Phố",
        domain="[('country_id', '=', 'vn')]")

    @api.depends('current_address', 'current_ward_id', 'current_district_id', 'current_state_id')
    def _compute_address(self):
        address = ''
        ward = ''
        district = ''
        city = ''
        if self.current_address:
            address = self.current_address + ", "
        if self.current_ward_id:
            ward = self.current_ward_id.name + ", "
        if self.current_district_id:
            district = self.current_district_id.name + ", "
        if self.current_state_id:
            city = self.current_state_id.name
        for a in self:
            a.name = address + ward + district + city