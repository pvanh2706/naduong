odoo.define('mvb_eoffice.update', function (require) {
    "use strict";
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var MailManager1 = require('mail_test.Manager');
    var session = require('web.session');

    var user = session.uid;

    MailManager1.include({
        _listenOnBuses: function(){
            this._super.apply(this, arguments);
            this.call('bus_service', 'onNotification', this, this.checkType);
        },
        checkType: function(data){
//            console.log("data check type 2", data, data === null, data === '', typeof data);
            if (data !== null
                && typeof data[0] !== 'undefined'
                && typeof data[0][1] !== 'undefined'
                && typeof data[0][1]['type'] !== 'undefined') {
                var type_doc = data[0][1]['type'];
                this.count_data_dashboard(type_doc);
                this.get_notify_create();
            }
        },
        get_notify_create: function(data) {
            self = this;
            rpc.query({
                model: 'one.signal.notification.messages',
                method: 'search_count_notify',
                args: [
                    {"id": user}
                ],
            }).then(function (data_count) {
                console.log("data count", data_count);
                if(parseInt(data_count) > 0) {
                    $('.o_notification_counter_notify').text(data_count);
                } else {
                    $('.o_notification_counter_notify').text("");
                }
            });
        },
        count_data_dashboard: function(type){
            if (type !== "" && typeof type !== 'undefined') {
                rpc.query({
                    model: 'dash.board.action.wizards',
                    method: 'default_get',
                    args: [["count_document_text_incoming",
                            "count_incoming_solution",
                            "count_document_deadline",
                            "count_incoming_follow",
                            "count_document_notification",
                            "count_document_text_outgoing",
                            "count_outgoing_solution",
                            "count_document_outgoing_deadline",
                            "view_calendar"]],
                }).then(function (data_count) {
                    console.log("data count dashboard 12356", data_count);
//                    $(".count_document_text_incoming").text(data_count.count_document_text_incoming);
//                    $(".count_incoming_solution").text(data_count.count_incoming_solution);
//                    $(".count_document_deadline").text(data_count.count_document_deadline);
//                    $(".count_incoming_follow").text(data_count.count_incoming_follow);
//                    $(".count_document_notification").text(data_count.count_document_notification);
//                    $(".count_document_text_outgoing").text(data_count.count_document_text_outgoing);
//                    $(".count_outgoing_solution").text(data_count.count_outgoing_solution);
//                    $(".count_document_outgoing_deadline").text(data_count.count_document_outgoing_deadline);
//                    alert($('span[name="count_incoming_solution"]')).text());
                    $('span[name="count_document_text_incoming"]').text(data_count.count_document_text_incoming);
                    $('span[name="count_incoming_solution"]').text(data_count.count_incoming_solution);
                    $('span[name="count_document_deadline"]').text(data_count.count_document_deadline);
                    $('span[name="count_incoming_follow"]').text(data_count.count_incoming_follow);
                    $('span[name="count_document_notification"]').text(data_count.count_document_notification);
                    $('span[name="count_document_text_outgoing"]').text(data_count.count_document_text_outgoing);
                    $('span[name="count_outgoing_solution"]').text(data_count.count_outgoing_solution);
                    $('span[name="count_document_outgoing_deadline"]').text(data_count.count_document_outgoing_deadline);
                });
            }
        },
    });
    return MailManager1;
});