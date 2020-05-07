from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import datetime


class DocumentController(http.Controller):
    @http.route('/mvb_eoffice/mvb_incoming_text_waiting_solution', auth='user', type='json')
    def document_solution_banner(self):
        document_now = datetime.now()
        name_user = request.env['res.users'].browse(request._uid).name
        count_doc_waiting = request.env['mvb.people.processing.text'].search_count(
            [('name', '=', name_user), ('check_work', '=', False), ('deadline', '>', document_now)])
        count_doc_deadline = request.env['mvb.people.processing.text'].search_count(
            [('name', '=', name_user), ('check_work', '=', False), ('deadline', '<', document_now)])

        return {
            'html': """
            <div class="row">
            <div class="col-md-1 col-sm-6">
            </div>
            <div class="col-md-5 col-sm-6 oh-payslip">
                <div class="oh-card">
                    <div class="oh-card-body">
                        <div class="stat-widget-one">
                            <div class="stat-icon stat-icon_1"><i class="fa fa-book"/></div>
                            <div class="stat-content">
                                <div class="stat-text">Chưa xử lý</div>
                                <div class="stat-digit">%s</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-5 col-sm-6 oh-payslip oh-broad-factor">
                <div class="oh-card">
                    <div class="oh-card-body">
                        <div class="stat-widget-one">
                            <div class="stat-icon stat-icon_1"><i class="fa fa-clock-o"/></div>
                            <div class="stat-content">
                                <div class="stat-text">Quá hạn xử lý</div>
                                <div class="stat-digit">%s</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-1 col-sm-6">
            </div>
            </div>
            """
                    % (count_doc_waiting, count_doc_deadline)
        }

    @http.route('/mvb_eoffice/mvb_incoming_text_follow', auth='user', type='json')
    def document_follow_banner(self):
        name_user = request.env['res.users'].browse(request._uid).name
        count_doc_follow = request.env['mvb.people.processing.text'].search_count(
            [('name', '=', name_user), ('state', '=', 'theodoi')])
        return {
            'html': """
            
                <div class="row">
                <div class="col-md-3 col-sm-6">
                </div>
                <div class="col-md-6 col-sm-6 oh-payslip oh-timesheets">
                    <div class="oh-card">
                        <div class="oh-card-body">
                            <div class="stat-widget-one">
                                <div class="stat-icon stat-icon_1"><i class="fa fa-clock-o"/></div>
                                <div class="stat-content">
                                    <div class="stat-text">Văn bản đang theo dõi</div>
                                    <div class="stat-digit">%s</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                </div>
                </div>
                """
                    % (count_doc_follow)

        }

    @http.route('/mvb_eoffice/mvb_draft_text_go_waiting_solution', auth='user', type='json')
    def document_draft_solution_banner(self):
        document_now = datetime.now()
        name_user = request.env['res.users'].browse(request._uid).name
        count_doc_draft_waiting = request.env['mvb.people.processing.textdraft'].search_count(
            [('name', '=', name_user), ('state', '=', 'chuaxuly'), ('dead_line', '>', document_now)])
        count_doc_draft_deadline = request.env['mvb.people.processing.textdraft'].search_count(
            [('name', '=', name_user), ('state', '=', 'chuaxuly'), ('dead_line', '<', document_now)])

        return {
            'html': """
                  <div class="row">
            <div class="col-md-1 col-sm-6">
            </div>
            <div class="col-md-5 col-sm-6  oh-payslip oh-contracts">
                <div class="oh-card">
                    <div class="oh-card-body">
                        <div class="stat-widget-one">
                            <div class="stat-icon stat-icon_1"><i class="fa fa-book"/></div>
                            <div class="stat-content">
                                <div class="stat-text">Chưa xử lý</div>
                                <div class="stat-digit">%s</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-5 col-sm-6  oh-payslip oh-contracts">
                <div class="oh-card">
                    <div class="oh-card-body">
                        <div class="stat-widget-one">
                            <div class="stat-icon stat-icon_1 stat-icon_x"><i class="fa fa-clock-o"/></div>
                            <div class="stat-content">
                                <div class="stat-text stat-text_1">Quá hạn xử lý</div>
                                <div class="stat-digit">%s</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-1 col-sm-6">
            </div>
            </div>
                   <div class="col-md-3 col-sm-6">
                   </div>
                   </div>
                   """
                    % (count_doc_draft_waiting, count_doc_draft_deadline)

        }
