odoo.define('my_calendar.menu.tree', function(require) {
    "use strict";
    var ListController = require("web.ListController");
    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName === "doimoi.work.calendar" && this.initialState.domain[0][2] === "confirm") {
                var summary_apply_leave_btn = this.$buttons.find('button.o_total_calendar_button');
                summary_apply_leave_btn.on('click', this.proxy('total_calendar_button'));
            }
        },
        total_calendar_button: function () {
            var self = this;
            var action = {
                type: "ir.actions.act_window",
                name: "Tổng hợp lịch",
                res_model: "doimoi.total.calendar.wizards",
                target: 'new',
                views: [[false, 'form']],
                view_mode: 'form',
            };
             return this.do_action(action);
        },
    };
    ListController.include(includeDict);
});