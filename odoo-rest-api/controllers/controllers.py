# -*- coding: utf-8 -*-
import json
import math
import logging
import requests
import datetime
import base64
import binascii

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    import dictfier
except ImportError as err:
    _logger.debug(err)

current_session = {}
current_context = {}

def flat_obj(obj, parent_obj, field_name):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d-%H-%M")
    if isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, datetime.time):
        return obj.strftime("%H-%M-%S")

    if hasattr(parent_obj, "fields_get"):
        field = parent_obj.fields_get(field_name)[field_name]
        field_type = field["type"]
        if field_type == "many2one":
            return obj.id
        if field_type in ["one2many", "many2many"]:
            return [rec.id for rec in obj]
        if field_type == "binary" and obj:
            return obj.decode("utf-8")

    return obj


def nested_flat_obj(obj, parent_obj):
    return obj


def nested_iter_obj(obj, parent_obj):
    return obj


class OdooAPI(http.Controller):
    @http.route('/auth/',
                type='json', auth='public',
                methods=["POST"], csrf=False, sitemap=False)
    def authenticate(self, *args, **post):
        login = post["login"]
        password = post["password"]
        try:
            db = request.env.cr.db
        except Exception:
            if "db" in post:
                db = post["db"]
            else:
                msg = (
                    "Looks like db is not properly configured, "
                    "you can pass its name to `db` parameter to "
                    "avoid this error!."
                )
                return {"Error": msg}

        url_root = request.httprequest.url_root
        AUTH_URL = f"{url_root}web/session/authenticate/"

        headers = {'Content-type': 'application/json'}

        data = {
            "jsonrpc": "2.0",
            "params": {
                "login": login,
                "password": password,
                "db": db
            }
        }

        res = requests.post(
            AUTH_URL,
            data=json.dumps(data),
            headers=headers
        )

        try:
            session_id = res.cookies["session_id"]
            user = json.loads(res.text)
            user["result"]["session_id"] = session_id
        except Exception:
            return "Invalid credentials."
        return user["result"]

    @http.route('/object/<string:model>/<string:function>',
                type='json', auth='public',
                methods=["POST"], csrf=False, sitemap=False)
    def call_model_function(self, model, function, **post):
        args = []
        kwargs = {}
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]
        model = request.env[model]
        result = getattr(model, function)(*args, **kwargs)
        return result

    @http.route('/object/<string:model>/<int:rec_id>/<string:function>',
                type='json', auth='public',
                methods=["POST"], csrf=False, sitemap=False)
    def call_obj_function(self, model, rec_id, function, **post):
        args = []
        kwargs = {}
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]
        obj = request.env[model].browse(rec_id).ensure_one()
        result = getattr(obj, function)(*args, **kwargs)
        return result

    @http.route(
        '/api/<string:model>',
        auth='public', methods=["GET"], csrf=False)
    def get_model_data(self, model, **params):
        records = request.env[model].search([])
        if "query" in params:
            query = json.loads(params["query"])
        else:
            query = [records.fields_get_keys()]

        if "exclude" in params:
            exclude = json.loads(params["exclude"])
            for field in exclude:
                if field in query[0]:
                    field_to_exclude = query[0].index(field)
                    query[0].pop(field_to_exclude)

        if "filter" in params:
            filters = json.loads(params["filter"])
            records = request.env[model].search(filters)

        prev_page = None
        next_page = None
        total_page_number = 1
        current_page = 1

        if "page_size" in params:
            page_size = int(params["page_size"])
            count = len(records)
            total_page_number = math.ceil(count / page_size)

            if "page" in params:
                current_page = int(params["page"])
            else:
                current_page = 1  # Default page Number
            start = page_size * (current_page - 1)
            stop = current_page * page_size
            records = records[start:stop]
            next_page = current_page + 1 \
                if 0 < current_page + 1 <= total_page_number \
                else None
            prev_page = current_page - 1 \
                if 0 < current_page - 1 <= total_page_number \
                else None

        if "limit" in params:
            limit = int(params["limit"])
            records = records[0:limit]

        data = dictfier.dictfy(
            records,
            query,
            flat_obj=flat_obj,
            nested_flat_obj=nested_flat_obj,
            nested_iter_obj=nested_iter_obj
        )

        res = {
            "count": len(records),
            "prev": prev_page,
            "current": current_page,
            "next": next_page,
            "total_pages": total_page_number,
            "result": data
        }
        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )

    @http.route(
        '/api/<string:model>/<int:rec_id>',
        auth='user', methods=["GET"], csrf=False)
    def get_model_rec(self, model, rec_id, **params):
        records = request.env[model].search([])
        if "query" in params:
            query = json.loads(params["query"])
        else:
            query = records.fields_get_keys()

        if "exclude" in params:
            exclude = json.loads(params["exclude"])
            for field in exclude:
                if field in query:
                    field_to_exclude = query.index(field)
                    query.pop(field_to_exclude)

        record = records.browse(rec_id).ensure_one()
        data = dictfier.dictfy(
            record,
            query,
            flat_obj=flat_obj,
            nested_flat_obj=nested_flat_obj,
            nested_iter_obj=nested_iter_obj
        )
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    @http.route(
        '/api/<string:model>/',
        type='json', auth='public',
        methods=['POST'], website=True, csrf=False)
    def post_model_data(self, model, **post):
        print('test')
        try:
            # Update function
            if (model == 'mvb.document'):
                if post.get('data'):
                    if post['data'].get('document_type'):
                        get_type = request.env['mvb.document.type'].sudo().search(
                            [('name', '=', post['data']['document_type'])])
                        if get_type:
                            post['data'].update({'document_type': get_type.id})

                    if post['data'].get('unit_promulgate'):
                        get_data = request.env['mvb.document.publisher'].sudo().search(
                            [('name', '=', post['data']['unit_promulgate'])])
                        if get_data:
                            post['data'].update({'unit_promulgate': get_data.id})

                    if post['data'].get('document_notebook'):
                        get_data = request.env['mvb.document.notebook'].sudo().search(
                            [('name', '=', post['data']['document_notebook'])])
                        if get_data:
                            post['data'].update({'document_notebook': get_data.id})

                    if post['data'].get('share_user'):
                        share_user = post['data']['share_user'].split(',')
                        list_user_ids = []
                        for i in share_user:
                            id_user = request.env['res.users'].sudo().search([('login', '=', i.strip())])
                            if id_user:
                                list_user_ids.append(id_user.id)
                        if list_user_ids:
                            post['data'].update({'share_user': [(6, 0, list_user_ids)]})

            elif model == 'mvb.incoming.text':
                _dict_type_document = {'draft_document': 'Bản thảo', 'course_document': 'Bản chính',
                                       'course_document_same': 'Bản sao y bản chính', 'document_coppy': 'Bản trích sao',
                                       'document_coppy_2': 'Bản sao lục'}
                _dict_urgency = {'thuong': 'Thường', 'khan': 'Khẩn', 'thuongkhan': 'Thượng khẩn', 'hoatoc': 'Hỏa tốc', 'hoatochengio': 'Hỏa tốc hẹn giờ'}
                _dict_security_level = {'mat': 'Mật', 'domat': 'Tối mật', 'tuyemat': 'Tuyệt mật'}
                if post.get('data'):
                    if post['data'].get('document_notebook'):
                        get_notebook = request.env['mvb.document.notebook'].sudo().search(
                            [('name', '=', post['data']['document_notebook'])])
                        if get_notebook:
                            post['data'].update({'document_notebook': get_notebook.id})
                    if post['data'].get('promulgate_authority'):
                        get_content = request.env['mvb.document.publisher'].sudo().search(
                            [('name', '=', post['data']['promulgate_authority'])])
                        if get_content:
                            post['data'].update({'promulgate_authority': get_content.id})
                    if post['data'].get('from_document_id'):
                        get_form = request.env['mvb.document.type'].sudo().search(
                            [('name', '=', post['data']['from_document_id'])])
                        if get_form:
                            post['data'].update({'from_document_id': get_form.id})
                    if post['data'].get('type_document'):
                        for item in _dict_type_document.keys():
                            if _dict_type_document.get(item) == post['data'].get('type_document'):
                                post['data'].update({'type_document': item})
                    if post['data'].get('urgency'):
                        for word in _dict_urgency.keys():
                            if _dict_urgency.get(word) == post['data'].get('urgency'):
                                post['data'].update({'urgency': word})
                    if post['data'].get('security_level'):
                        for sec in _dict_security_level.keys():
                            if _dict_security_level.get(sec) == post['data'].get('security_level'):
                                post['data'].update({'security_level': sec})

            data = post['data']

        except KeyError:
            _logger.exception(
                "'data' parameter is not found on POST request"
            )

        if "context" in post:
            context = post["context"]
            record = request.env[model].sudo().with_context(**context).create(data)
        else:
            record = request.env[model].sudo().create(data)
            if record:
                if post['data'].get('data_attachment'):
                    for item in post['data'].get('data_attachment'):
                        name_attachment = item.get('name_attachment')
                        datas = item.get('data_file_base64')
                        try:
                            base64.b64decode(datas)
                            request.env['ir.attachment'].sudo().create([{'name': name_attachment,
                                                                  'datas': datas,
                                                                  'datas_fname': name_attachment,
                                                                  'res_model': model,
                                                                  'res_id': record.id}])
                        except Exception:
                            print('no correct base64')
                            continue
        return record.id

    @http.route(
        '/api/<string:model>/<int:rec_id>/',
        type='json', auth="user",
        methods=['PUT'], website=True, csrf=False)
    def put_model_record(self, model, rec_id, **post):
        try:
            data = post['data']
        except KeyError:
            _logger.exception(
                "'data' parameter is not found on PUT request"
            )

        if "context" in post:
            rec = request.env[model].with_context(**post["context"]) \
                .browse(rec_id).ensure_one()
        else:
            rec = request.env[model].browse(rec_id).ensure_one()

        for field in data:
            if isinstance(data[field], dict):
                operations = []
                for operation in data[field]:
                    if operation == "push":
                        operations.extend(
                            (4, rec_id, _)
                            for rec_id
                            in data[field].get("push")
                        )
                    elif operation == "pop":
                        operations.extend(
                            (3, rec_id, _)
                            for rec_id
                            in data[field].get("pop")
                        )
                    elif operation == "delete":
                        operations.extend(
                            (2, rec_id, _)
                            for rec_id
                            in data[field].get("delete")
                        )
                    else:
                        data[field].pop(operation)  # Invalid operation

                data[field] = operations
            elif isinstance(data[field], list):
                data[field] = [(6, _, data[field])]  # Replace operation
            else:
                pass

        if rec.exists():
            return rec.write(data)
        else:
            return False

    @http.route(
        '/api/<string:model>/',
        type='json', auth="user",
        methods=['PUT'], website=True, csrf=False)
    def put_model_records(self, model, **post):
        try:
            data = post['data']
        except KeyError:
            _logger.exception(
                "'data' parameter is not found on PUT request"
            )

        filters = post["filter"]
        rec = request.env[model].search(filters)

        if "context" in post:
            rec = request.env[model].with_context(**post["context"]) \
                .search(filters)
        else:
            rec = request.env[model].search(filters)

        for field in data:
            if isinstance(data[field], dict):
                operations = []
                for operation in data[field]:
                    if operation == "push":
                        operations.extend(
                            (4, rec_id, _)
                            for rec_id
                            in data[field].get("push")
                        )
                    elif operation == "pop":
                        operations.extend(
                            (3, rec_id, _)
                            for rec_id
                            in data[field].get("pop")
                        )
                    elif operation == "delete":
                        operations.extend(
                            (2, rec_id, _)
                            for rec_id in
                            data[field].get("delete")
                        )
                    else:
                        pass  # Invalid operation

                data[field] = operations
            elif isinstance(data[field], list):
                data[field] = [(6, _, data[field])]  # Replace operation
            else:
                pass

        if rec.exists():
            return rec.write(data)
        else:
            return False

    @http.route(
        '/api/<string:model>/<int:rec_id>/',
        type='http', auth="user",
        methods=['DELETE'], website=True, csrf=False)
    def delete_model_record(self, model, rec_id, **post):
        rec = request.env[model].browse(rec_id).ensure_one()
        if rec.exists():
            is_deleted = rec.unlink()
        else:
            is_deleted = False
        res = {
            "result": json.dumps(is_deleted)
        }
        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )

    @http.route(
        '/api/<string:model>/',
        type='http', auth="user",
        methods=['DELETE'], website=True, csrf=False)
    def delete_model_records(self, model, **post):
        filters = json.loads(post["filter"])
        rec = request.env[model].search(filters)
        if rec.exists():
            is_deleted = rec.unlink()
        else:
            is_deleted = False
        res = {
            "result": json.dumps(is_deleted)
        }
        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )

    @http.route(
        '/api/<string:model>/<int:rec_id>/<string:field>',
        type='http', auth="user",
        methods=['GET'], website=True, csrf=False)
    def get_binary_record(self, model, rec_id, field, **post):
        rec = request.env[model].browse(rec_id).ensure_one()
        if rec.exists():
            src = getattr(rec, field).decode("utf-8")
        else:
            src = False
        return http.Response(
            src
        )
