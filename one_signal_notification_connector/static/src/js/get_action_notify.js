odoo.define('mail_test.Manager', function (require) {
    "use strict";
    var AbstractService = require('web.AbstractService');
    var Bus = require('web.Bus');
    var core = require('web.core');

    var NotifyCreate =  AbstractService.extend({
        dependencies: ['ajax', 'bus_service', 'local_storage'],
        _ODOOBOT_ID: "ODOOBOT",
        start: function () {
            this._super.apply(this, arguments);
            this._listenOnBuses();
        },
        _listenOnBuses: function () {},
    });
    core.serviceRegistry.add('mail_service_1', NotifyCreate);
    return NotifyCreate;
});