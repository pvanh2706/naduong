odoo.define('quick_search_time_range.listview', function (require) {
"use strict";

var time        = require('web.time');
var core        = require('web.core');
var data        = require('web.data');
var session     = require('web.session');
var utils       = require('web.utils');
var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;
var config      = require('web.config');

var SearchView = require('web.SearchView');

function is_mobile() {
    return config.device.size_class <= config.device.SIZES.XS;
}

var SearchView          = require('web.SearchView');
var ListController      = require('web.ListController');

SearchView.include({
    build_search_data: function () {
//         debugger;
        var res = this._super();
//        Console.log("Viee anh ngu");
//         var res = this._super.apply(this, arguments);
        // console.log(this.tm723_domain);
        // console.log("AAAAAAAAAA3232323");
//         debugger;
        res.domains = res.domains.concat(this.tm723_domain || []);
//         debugger;
        return res;
    },
},
);

var SearchTimeRange = {

    RenderDateRangePicker: function(this2, node) {
        var self = this2;
        var range_field  = self.$tm723_time_range.find('.tm723_select_field').val();
        var tm723_is_datetime_field = self.tm723_fields[range_field] == 'datetime' ? true : false;
//         console.log("Thanhnd: RenderDateRangePicker");
//         debugger;
        var l10n                = _t.database.parameters,
//         searchview              = self.getParent().searchview,
//         searchview              = self.getParent().controllers.controller_3.widget.searchView,
        searchview              = self.searchView,
        datetime_format         = time.getLangDatetimeFormat(),
        server_datetime_format  = tm723_is_datetime_field ? 'YYYY-MM-DD HH:mm:ss' : 'YYYY-MM-DD';
        // console.log('CCCCCCCCCCCCCCCCCCCCCCCCC: ' + searchview);
        // debugger;
        searchview.tm723_domain = [];
//         searchview.query.trigger('reset');
        // debugger;
        self.$tm723_time_range.find('.tm723_time_field').css('width', tm723_is_datetime_field ? 225 : 150);
        self.$tm723_time_range.find('.tm723_time_field').daterangepicker({
            showDropdowns: true,
            timePicker: tm723_is_datetime_field,
            timePickerIncrement: 5,
            timePicker24Hour: true,
            startDate: moment().startOf('day'),
            endDate: moment().startOf('day'),
            locale : {
                format: tm723_is_datetime_field ? datetime_format.substring(0, 16): datetime_format.substring(0, 10),
                applyLabel: _t('Apply'),
                cancelLabel: _t('Cancel'),
                customRangeLabel: _t('Tùy chọn'),
            },
            // .set({hour:0,minute:0,second:0,millisecond:0})
            ranges: {
                'Hôm nay': [moment().startOf('day'), moment().endOf('day')],
                'Hôm qua': [moment().startOf('day').subtract(1, 'days'), moment().endOf('day').subtract(1, 'days')],
                '7 Ngày trước': [moment().startOf('day').subtract(6, 'days'), moment().endOf('day')],
                '30 ngày trước': [moment().startOf('day').subtract(29, 'days'), moment().endOf('day')],
                'Tháng này': [moment().startOf('month'), moment().endOf('month')],
                'Tháng trước': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        });
        var tm723_time_field = self.$tm723_time_range.find('.tm723_time_field')
        tm723_time_field.val('');
        tm723_time_field.on('cancel.daterangepicker', function(ev, picker) {
            tm723_time_field.val('');
            searchview.tm723_domain = [];
            searchview.query.trigger('reset');
        });
        tm723_time_field.on('apply.daterangepicker', function(ev, picker) {
            var start = moment(picker.startDate),
                end = moment(picker.endDate);
            if (self.tm723_fields[range_field] == 'datetime') {
                start.subtract(session.getTZOffset(start.format(server_datetime_format)), 'minutes');
                end.subtract(session.getTZOffset(end.format(server_datetime_format)), 'minutes');
            }
            // console.log(start.format(server_datetime_format), end.format(server_datetime_format))
            debugger;
            searchview.tm723_domain = [[[range_field,'>=',start.format(server_datetime_format)], [range_field,'<=',end.format(server_datetime_format)]]]
            searchview.query.trigger('reset');
        });
        self.$tm723_time_range.appendTo(node);
    },

}

ListController.include({

    renderButtons: function ($node) {
        var self = this;
        this._super.apply(this, arguments);
        self.tm723_fields = {};
        var tm723_fields = [], tmp_fields = {};
        _.each(self.initialState.fields, function(value, key, list){
            if (value.store && value.type === "datetime" || value.type === "date") {
                // console.log("Get cccccccccccccc");
                tmp_fields[key] = [value.type, value.string];
//                 debugger;
            }
        });

//         debugger;
        _.each(self.initialState.fieldsInfo.list, function(value, key, list){
            console.log("Each 2 ---------");
//             debugger;
            if (!value.modifiers.column_invisible && tmp_fields[key]) {
                self.tm723_fields[ key ] = tmp_fields[key][0];
                tm723_fields.push([key, value.string ||  tmp_fields[key][1]]);
            }
        });

        if (tm723_fields.length > 0) {
            self.$tm723_time_range = $(QWeb.render('tm723.SearchTimeRange', {'tm723_fields': tm723_fields}))
            // console.log("Thanhnd:  1111111"),
            SearchTimeRange.RenderDateRangePicker(self, self.$buttons);
            // console.log("Thanhnd:  2222222"),
            self.$tm723_time_range.find('.tm723_select_field').on('change', function() {
                SearchTimeRange.RenderDateRangePicker(self, self.$buttons);
            })

        }
    },

});

var PivotController      = require('web.PivotController');

PivotController.include({

    renderButtons: function ($node) {
        var self = this;
        this.$tm723_node = $node;
        this._super.apply(this, arguments);
        self.tm723_fields = {};
        var tm723_fields = [];
        _.each(self.initialState.fields, function(value, key, list){
            if (value.store && value.type === "datetime" || value.type === "date") {
                self.tm723_fields[ value.name ] = value.type;
                tm723_fields.push([value.name, value.string]);
            }
        });
        if (tm723_fields.length > 0) {
            self.$tm723_time_range = $(QWeb.render('tm723.SearchTimeRange', {'tm723_fields': tm723_fields}))
            SearchTimeRange.RenderDateRangePicker(self, self.$buttons.find('.o_pivot_download').parent());
            self.$tm723_time_range.find('.tm723_select_field').on('change', function() {
                SearchTimeRange.RenderDateRangePicker(self, self.$buttons.find('.o_pivot_download').parent());
            })

        }
    },

});

var KanbanController      = require('web.KanbanController');

KanbanController.include({

    renderButtons: function ($node) {
        var self = this;
        this.$tm723_node = $node;
        this._super.apply(this, arguments);

        self.tm723_fields = {};
        var tm723_fields = [], tmp_fields = {};
        _.each(self.initialState.fields, function(value, key, list){
            if (value.store && value.type === "datetime" || value.type === "date") {
                tmp_fields[value.name] = [value.type, value.string];
            }
        });
        _.each(self.initialState.fieldsInfo.kanban, function(value, key, list){
            if (!value.modifiers.column_invisible && tmp_fields[value.name]) {
                self.tm723_fields[ value.name ] = tmp_fields[value.name][0];
                tm723_fields.push([value.name, value.string || tmp_fields[value.name][1]]);
            }
        });

        if (tm723_fields.length > 0) {
            self.$tm723_time_range = $(QWeb.render('tm723.SearchTimeRange', {'tm723_fields': tm723_fields}))
            SearchTimeRange.RenderDateRangePicker(self, self.$buttons);
            self.$tm723_time_range.find('.tm723_select_field').on('change', function() {
                SearchTimeRange.RenderDateRangePicker(self, self.$buttons);
            })

        }
    },

});


});