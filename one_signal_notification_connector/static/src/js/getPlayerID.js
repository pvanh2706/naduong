odoo.define('one_signal_notification_connector.reconciliationrenderer', function (require) {
    "use strict";
    
    var core = require('web.core');
    var ListView = require('web.ListView');
    var ListController = require("web.ListController");
    var rpc = require('web.rpc');
    var qweb = core.qweb;
    var session = require('web.session');
    var user = session.uid

    var id_player = OneSignal.getUserId();
   
    id_player.then(function (v) {
        var values = [{
            active: true,
            company_id: session.company_id,
            name: v,
            user_id: session.uid,
        }];
        rpc.query({
            model: 'one_signal_notification.users_device_ids',
            method: 'create',
            args: values
        }).then(function (returned_value) {
            console.log('done', returned_value);
        });
    });
});