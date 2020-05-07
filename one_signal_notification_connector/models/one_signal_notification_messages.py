from odoo import api, fields, models, _
import requests
import json
import logging
import ast
from odoo.http import request
_logger = logging.getLogger(__name__)

SPECIFIC_DEVICES = [
    ('include_player_ids', 'include_player_ids'),
    ('include_email_tokens', 'include_email_tokens'),
    ('include_external_user_ids', 'include_external_user_ids')
]


class OneSignalNotification(models.Model):
    _name = "one.signal.notification.messages"
    _rec_name = 'contents'
    _description = 'one signal notification messages'

    @api.model
    def _get_company(self):
        return self.env.user.company_id

    # Segments
    included_segments = fields.Char(string="Include Segments", required=False,
                                    default=["Active Users", "Inactive Users"],
                                    help="App Segments such as 'All', 'Active Users', 'Inactive Users'")
    excluded_segments = fields.Char(string="Exclude Segments", required=False,
                                    help="App Segments such as 'All', 'Active Users', 'Inactive Users'")

    # Filters
    filter = fields.Char(string="Filter", required=False, help="Filters is condition on which device are picked")

    # Specific Devices
    specific_devices = fields.Selection(string="Specific Devices", selection=SPECIFIC_DEVICES, required=False)
    user_ids = fields.Many2many(comodel_name="res.users", relation="one_signal_notification_res_users_rel",
                                column1="message_id", column2="user_id", string="Users", )
    target_parameters = fields.Char(string="Target Parameters", required=False, help="List of specific device")

    contents = fields.Char(string="Contents", required=True, help="Content display to end user")
    headings = fields.Char(string="Headings", required=False, help="Heading display to end user")
    data = fields.Char(string="Data", required=False,
                       help="Is used to process on the backend(OnClick navigation to the screen)")

    app_id = fields.Many2one(comodel_name="one.signal.notification.apps", string="App", required=False,
                             help="Message send to the application")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=False, default=_get_company)

    status = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('sent', 'Sent'), ('fail', 'Failed'), ],
                              required=False, default="draft", help="Status of the notification")
    web_url = fields.Char(string="Web_URL",required=False)
    is_read = fields.Boolean(string= "Đã đọc", default= False)

    # Response from One Signal
    reason = fields.Text(string="Reason", required=False, help="Response of the Notification")
    external_id = fields.Char(string="One Signal External Id", required=False, )
    one_signal_notification_id = fields.Char(string="Notification Id", required=False, )
    recipients_count = fields.Integer(string="Recipients Count", required=False)

    @api.model
    def create(self, values):
        res = super(OneSignalNotification, self).create(values)
        self.env['bus.bus'].sendmany([[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': []}]])
        # print("đã tạooooooooooooooooo 5")
        return res

    @api.model
    def search_count_notify(self, user):
        res = self.env['one.signal.notification.messages'].search_count([("is_read","=",False),("user_ids","=",user['id'])])
        return res

    @api.model
    def write_notifi(self, idItem):
        self.env['one.signal.notification.messages'].search([("id","=",idItem["id"])]).write({"is_read": True})
        return self.is_read

    def onchange_included_segments(self):
        self.excluded_segments = False
        self.filter = False
        self.specific_devices = False

    @api.onchange("filter")
    def onchange_filter(self):
        self.included_segments = False
        self.excluded_segments = False
        self.specific_devices = False

    @api.onchange("specific_devices")
    def onchange_specific_devices(self):
        self.included_segments = False
        self.excluded_segments = False
        self.filter = False
        self.user_ids = False

    @api.onchange("user_ids")
    def onchange_users(self):
        result = []
        search_condition = [("user_id", "in", self.user_ids.ids)]
        one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(search_condition)
        for current_record in one_signal_user_object:
            if self.specific_devices == "include_player_ids":
                result.append(current_record.name)
            elif self.specific_devices == "include_email_tokens":
                result.append(current_record.user_id.login)
            elif self.specific_devices == "include_external_user_ids":
                result.append(str(current_record.user_id.id))
        self.target_parameters = result

    @api.multi
    def send_message(self):
        data = {}
        # data = {
        #     'content': {},
        #     'headings': {},
        #     'data': {},
        #     'included_segments': [],
        #     'excluded_segments': [],
        #     'filters': [],
        #     'specific_devices_key': False,
        #     'specific_devices_list': [],
        # }
        search_condition = [("active", "=", True)]
        if self.app_id:
            search_condition.append(("id", "=", self.app_id.id))
        else:
            search_condition.append(("company_id", "=", self.env.user.company_id.id))

        apps_object = self.env['one.signal.notification.apps']

        for app_record in apps_object.search(search_condition, limit=1):
            data['app_api_key'] = app_record.app_api_key
            data['app_id'] = app_record.app_id

        if self.included_segments:
            data['included_segments'] = ast.literal_eval(self.included_segments)
        if self.excluded_segments:
            data['excluded_segments'] = ast.literal_eval(self.excluded_segments)
        if self.filter:
            data['filter'] = ast.literal_eval(self.filter)
        data['contents'] = ast.literal_eval(self.contents)
        if self.web_url:
            data['web_url'] = self.web_url
        if self.headings:
            data['headings'] = ast.literal_eval(self.headings)
        if self.data:
            data['data'] = ast.literal_eval(self.data)
        if self.specific_devices and self.target_parameters:
            data['specific_devices_key'] = self.specific_devices
            data['specific_devices_list'] = ast.literal_eval(self.target_parameters)
        response = self.send_notification(data)
        response_json = response.json()
        if response.status_code == 200:
            self.status = "sent"
            self.reason = str(response.status_code) + " " + str(response.reason)

            self.external_id = response_json.get('external_id', False) or False
            self.one_signal_notification_id = response_json['id'] or False
            self.recipients_count = response_json['recipients'] or False
            if 'errors' in response_json:
                self.reason += " " + str(response_json['errors'])
            if 'warnings' in response_json:
                self.reason += " " + str(response_json['warnings'])
        else:
            self.status = "fail"
            self.reason = str(response.status_code) + " " + str(response.reason) + " " + str(response_json['errors'])
            self.external_id = False
            self.one_signal_notification_id = False
            self.recipients_count = False
            if 'warnings' in response_json:
                self.reason += " " + str(response_json['warnings'])
        return True

    @api.one
    def action_retry(self):
        self.status = "draft"

    @api.model
    def lead_to_url(self,itemId):
        holder = self.env['one.signal.notification.messages'].search([('id', '=', itemId['id'])])
        url_web = holder.web_url
        print("link in python file:",url_web)
        return url_web

    @staticmethod
    def send_notification(data):
        header = {}
        response = False
        payload = {}

        app_id = data.get('app_id', False) or False
        app_api_auth_key = data.get('app_api_key', False) or False
        if app_id and app_api_auth_key:
            header = {"Content-Type": "application/json; charset=utf-8",
                      "Authorization": "Basic %s" % app_api_auth_key}
            payload["app_id"] = app_id
            if data.get("included_segments", False) or False:
                payload["included_segments"] = data.get("included_segments")
            payload["excluded_segments"] = data.get("excluded_segments", []) or []

            notification_filter = data.get("filter", []) or []
            if isinstance(notification_filter, list):
                payload["filters"] = notification_filter

            else:
                _logger.info("Filter is not applied")
                _logger.info("Please provide Input Request field 'filter' in the List of dictionary format eg: [{}, {}]"
                             "to the send_notification() method")
            specific_devices = data.get('specific_devices_key', False) or False
            specific_devices_list = data.get('specific_devices_list', []) or []

            if isinstance(specific_devices_list, list) and specific_devices:
                payload[specific_devices] = specific_devices_list
            elif specific_devices:
                _logger.info("specific_devices is not applied")
                _logger.info("Please provide Input Request field 'specific_devices' in String and "
                             "'specific_devices_list' in the List eg: [, ] "
                             "to the send_notification() method")

            if data.get("contents" or False) or False:
                payload['contents'] = data.get("contents")
            else:
                _logger.info('Please provide the "contents" '
                             'eg: {"en": "English Message", "es": "Spanish Message"} '
                             'in the Input Request to the send_notification() method')
            if data.get("headings" or False) or False:
                payload['headings'] = data.get("headings")
            else:
                _logger.info('Please provide the "headings" '
                             'eg: {"en": "English Title", "es": "Spanish Title"} '
                             'in the Input Request to the send_notification() method')
                             
            if data.get("web_url" or False) or False:
                payload['web_url'] = data.get("web_url")
            else:
                _logger.info('Please provide the "web_url" '
                             'eg: {"en": "English Title", "es": "Spanish Title"} '
                             'in the Input Request to the send_notification() method')

            if data.get("data" or False) or False:
                payload['data'] = data.get("data")
            else:
                _logger.info('Please provide the "data" '
                             'eg: {"en": "English Title", "es": "Spanish Title"} '
                             'in the Input Request to the send_notification() method')



        else:
            _logger.info('Please provide the "app_id" & "app_api_key" in the Input Request to the '
                         'send_notification() method')

        if header and payload:
            payload = json.dumps(payload)
            response = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=payload)
            _logger.info("Response: %s" % str(response.status_code)+" "+str(response.reason))
            _logger.info("Response Json: %s" % str(response.json()))

            # return str(response.status_code)+" "+str(response.reason)

        return response


