# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class MyCalendar(http.Controller):
    # @http.route('/my_calendar/button_total_calendar', auth='user', type='json')
    # def button_total_calendar_banner(self):
    #     return {
    #         'html': """
    #            <div class="col-md-5 col-sm-6 o_total_calendar_button oh-payslip">
    #                <div class="oh-card">
    #                    <div class="oh-card-body">
    #                        <div class="stat-widget-one">
    #                            <div class="stat-icon stat-icon_1"><i class="fa fa-book"/></div>
    #                            <div class="stat-content">
    #                                <div class="stat-text">Tổng hợp lịch</div>
    #                            </div>
    #                        </div>
    #                    </div>
    #                </div>
    #            """
    #     }
    @http.route('/my_calendar/document_video', auth='user', type='json')
    def document_video_banner(self):
        return {
            'html': """
                    <div>
                     <link>
                    <center>
                    <h1>font color="red"> Like & Subscribe The Channel ......!</font></h1>
                    </center>
                    <center>
                    <p><font color="blue"><a href="https://www.youtube.com/watch?v=Suyekbyj1cs&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=109"> Bạn hãy kích vào đây</a></p>
                    </font>
                    </div>
                    </center>
                        """
        }
