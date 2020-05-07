
odoo.define('one_signal_notification_1.icons', function (require) {
    "use strict";
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var session = require('web.session');

    var user = session.uid;

    var previews = [];
    window.click_num = 0;

    var ActionMenu = Widget.extend({
        template: 'systray_cloud.myicon',//provide the template name
        events: {
            'click .new_icon': 'onclick_myicon',
            'click .o_mail_preview': 'onclick_notify_item',
            'show.bs.dropdown': 'onclick_myicon',
        },
        start: function () {
            this._$previews = this.$('.o_mail_systray_dropdown_items');
            this.get_data();
            this.get_notify();

        },
        get_notify: function () {
            self = this;
            rpc.query({
                model: 'one.signal.notification.messages',
                method: 'search_count_notify',
                args: [
                    {
                        "id": user
                    }
                ],
            }).then(function (data_count) {
                // print("data count----------", data_count)
                if (parseInt(data_count) > 0) {
                    $('.o_notification_counter_notify').text(data_count);
                } else {
                    $('.o_notification_counter_notify').text("");
                }
            });
        },
        dynamicSort: function (property) {
            return function (a, b) {
                return (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
            }
        },
        get_data: function () {
            var self = this;
            // var domain = [(user, 'in', 'user_ids')];
            // var args = [domain];
            rpc.query({
                model: 'one.signal.notification.messages',
                method: 'search_read',
                // args: [domain]
            }).then(function (data) {
                data.sort((a, b) => (a.id < b.id) ? 1 : -1);
               // console.log("data--------------", data);
                previews = [];
                if (data.length > 0) {
                    data.forEach(element => {
                        if (element.user_ids.length > 0) {
                            element.user_ids.forEach(item => {
                                if (item == user) {
                                    var string_name = JSON.parse(element.headings.replace(/'/g, '"'))['en'];
                                    var index_slit_name = string_name.indexOf("\n");
                                    var title_notify = string_name.slice(index_slit_name);
                                    try {
                                        previews.push({
                                            body: JSON.parse(element.contents.replace(/'/g, '"'))['en'],
                                            id: element.id,
                                            imageSRC: "/one_signal_notification_connector/static/src/img/logo.png",
                                            status: "bot",
                                            title: title_notify,
                                            unreadCounter: element.is_read ? "" : 1,
                                        });
                                    } catch (error) {
                                        previews.push({
                                            body: '',
                                            id: element.id,
                                            imageSRC: "/one_signal_notification_connector/static/src/img/logo.png",
                                            status: "bot",
                                            title: title_notify,
                                            unreadCounter: element.is_read ? "" : 1,
                                        });
                                    }
                                }

                            });

                        }

                    });
                    return previews;
                }
            }).then(function () {
                self.showData();
            });
        },
        onclick_myicon: async function () {
            await this.get_data();
            await this.get_notify();
            // console.log("đã click", this.get_data());
            // this._$previews.html(QWeb.render('mail.systray.MessagingMenu.Previews', {
            //     previews: previews,
            // }));
        },
        showData: function () {
            this._$previews.html(QWeb.render('mail.systray.MessagingMenu.Previews', {
                previews: previews,
            }));
        },
        onclick_notify_item: function (ev) {
            self = this;
            var itemId = ev.currentTarget.dataset.previewId;
            rpc.query({
                model: 'one.signal.notification.messages',
                method: 'write_notifi',
                args: [
                    {
                        "id": itemId
                    }
                ],
            }).then(function (data) {
                self.get_data();
                self.get_notify();
            });
            rpc.query({
                model: 'one.signal.notification.messages',
                method: 'lead_to_url',
                args: [{ "id": itemId }],
            }).then(function (data) {
                self.do_action({
                    type: 'ir.actions.act_url',
                    target: 'self',
                    url: data
                });

            });
        },
    });
    SystrayMenu.Items.push(ActionMenu);//add icon to the SystrayMenu
    return ActionMenu;//return widget
});