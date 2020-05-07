odoo.define('my_contacts.menu.tree', function(require) {
    "use strict";
    var ListController = require("web.ListController");
    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            var self = this;
            self.$buttons.on('click', '.o_report_range_button', function () {
                self._rpc({
                    route: '/web/action/load',
                    params: {
                        action_id: 'mvb_eoffice.mvb_rage_date_wizards_action',
                    },
                })
                .then(function(r) {
                    console.log(r);
                    return self.do_action(r);
                });
            });
        }
    };
    ListController.include(includeDict);
});