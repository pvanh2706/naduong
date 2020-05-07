// alert("Vanh da sua o day");
odoo.define('preview_document_sidebar', function (require) {
"use strict";
/**
 * The feature is disabled as it was replaced by another feature
 * while still holding unfixed bugs and doing unnecessary rpc.
 */
// odoo 12 return;
// https://github.com/odoo/odoo/commit/1dbb555aab8910d1739783c39fd502c4a2e145d0

var core = require('web.core');
var Dialog = require('web.Dialog');
var framework = require('web.framework');
var Sidebar = require('web.Sidebar');
var field_utils = require('web.field_utils');
var rpc = require('web.rpc');
var chatter = require('mail.Chatter');
var mail_act = require('mail.systray.ActivityMenu')
var _t = core._t;

Sidebar.include({
    /**
     * @override
     */
    init : function (parent, options) {
        this._super.apply(this, arguments);
        this.hasAttachments = options.viewType === "form";
        if (this.hasAttachments) {
            this.sections.splice(1, 0, { 'name' : 'files', 'label' : _t('Attachment(s)'), });
            this.items.files = [];
            this.fileuploadId = _.uniqueId('oe_fileupload');
            $(window).on(this.fileuploadId, this._onFileUploaded.bind(this));
            console.log("11123123123", $("<a>").text());
        }
    },
    /**
     * Get the attachment linked to the record when the toolbar started
     *
     * @override
     */
    start: function () {
        var _super = this._super.bind(this);
        var def = this.hasAttachments ? this._updateAttachments() : $.when();
        return def.then(_super);
    },
    /**
     * @override
     */
    destroy: function () {
        if (this.hasAttachments) {
            $(window).off(this.fileuploadId);
        }
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------
    /**
     * @override
     */
    updateEnv: function (env) {
        this.env = env;
        var _super = _.bind(this._super, this, env);
        var def = this.hasAttachments ? this._updateAttachments() : $.when();
        def.then(_super);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Process the attachments then rerender the toolbar
     *
     * @private
     * @param  {Object} attachments
     */
    _processAttachments: function (attachments) {
        //to display number in name if more then one attachment which has same name.
        var self = this;
        _.chain(attachments)
            .groupBy(function (attachment) { return attachment.name; })
            .each(function (attachment) {
                 if (attachment.length > 1) {
                    _.map(attachment, function (attachment, i) {
                        attachment.name = _.str.sprintf(_t("%s (%s)"), attachment.name, i+1);
                    });
                }
            });
        _.each(attachments,function (a) {
            a.label = a.name;
            if (a.type === "binary") {
                a.url = '/web/content/'  + a.id + '?download=true';
            }
            a.create_date = field_utils.parse.datetime(a.create_date, 'create_date', {isUTC: true});
            a.create_date_string = field_utils.format.datetime(a.create_date, 'create_date', self.env.context.params);
            a.write_date = field_utils.parse.datetime(a.write_date, 'write_date', {isUTC: true});
            a.write_date_string = field_utils.format.datetime(a.write_date, 'write_date', self.env.context.params);
        });
        this.items.files = attachments;
    },
    /**
     * @private
     * @override
     */
    
    
    
    _redraw: function () {
        this._super.apply(this, arguments);
        // $(".o_dropdown_menu").attr("position","relative");
        // $('a[data-section="files"]').wrapAll("<div></div>");
        // $('a[data-section="files"]').before("<span style='float: left' class='fas fa-address-card o_sidebar_preview_attachment'/>");
        // $("<label><span style='float: left' class='fas fa-address-card'/><label>").appendTo('a[data-section="files"]');
        
        // $(".o_dropdown_menu").attr("color","red");
        _.each(this.$('a[data-section="files"]'), function (el,index) {
            var dataUrl = $('a[data-index='+index+'][data-section="files"]').attr("href");
            $('a[data-index='+index+'][data-section="files"]').css("padding-left","35px");
            $('a[data-index='+index+'][data-section="files"]').css("padding-right","30px");
            // console.log(index, "dataUrl---", dataUrl);
            // if($('a[data-index='+index+']').attr("data-section") === 'files'){
            //     this.wrapAll("<div></div>");
            // }
            // $('a[data-index='+index+']:first').wrapAll("<div style='border: 1px solid red'></div>");
            // $('a[data-index='+index+']').before("<span style='float: left' data-url='"+dataUrl+"' class='fa fa-eye o_sidebar_preview_attachment'/>");
            $("<span title='Xem tệp đính kèm' role='img' data-url='"+dataUrl+"' aria-label='View File' style='padding: 0px;position: absolute;top: 5px;left:3px' class='fa fa-file-text-o o_sidebar_preview_attachment'/>").appendTo('a[data-index='+index+'][data-section="files"]');
            $("<span title='Tải xuống tệp đính kèm' role='img' data-url='"+dataUrl+"' aria-label='Download File' style='padding: 0px;position: absolute;top: 5px;left:19px' class='fa fa-download o_sidebar_download_attachment'/>").appendTo('a[data-index='+index+'][data-section="files"]');
            // $('.o_sidebar_delete_attachment').css("padding-left","5px");
            // $('a[data-section="files"]').css("float","left");
        });
        $().mouse
        if (this.hasAttachments) {
            this.$('.o_sidebar_add_attachment .o_form_binary_form')
                .change(this._onAddAttachment.bind(this));
            this.$('.o_sidebar_delete_attachment')
                .click(this._onDeleteAttachment.bind(this));
            this.$('.o_sidebar_preview_attachment')
                .click(this._onPreviewAttachment).bind(this);
            this.$('.o_sidebar_download_attachment')
                .click(this._onDownloadAttachment).bind(this);
        }
    },
    /**
     * Update the attachments to be displayed in the attachment section
     * of the toolbar
     *
     * @private
     */
    // 189900
    _updateAttachments: function () {
        if (this.items.files === undefined) {
            return $.when();
        }
        var activeId = this.env.activeIds[0];
        if (!activeId) {
            this.items.files = [];
            return $.when();
        } else {
            var domain = [
                ['res_model', '=', this.env.model],
                ['res_id', '=', activeId],
                ['type', 'in', ['binary', 'url']]
            ];
            var fields = ['name', 'url', 'type',
                'create_uid', 'create_date', 'write_uid', 'write_date'];
            return this._rpc({
                model: 'ir.attachment',
                method: 'search_read',
                context: this.env.context,
                domain: domain,
                fields: fields,
            }).then(this._processAttachments.bind(this));
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Method triggered when user click on 'add attachment' and select a file
     *
     * @private
     * @param  {Event} event
     */

    _onPreviewAttachment: function(event){
        event.preventDefault();
        var url = event.delegateTarget.dataset['url'];
        var findText = url.indexOf("?");
        url = url.slice(0, findText);
        var getIDText = url.lastIndexOf("/");
        var IdField = url.slice(getIDText+1);
        rpc.query({
            model: 'mvb.setting.preview',
            method: 'update_mimetype',
            args: [
                {"id_file": IdField}
            ],
        }).then(function(data){
            if (data == 1) {
                window.open(url,'_blank',);
            }
        });

        // var url = event.delegateTarget.dataset['url'];
        // var findText = url.indexOf("?");
        // url = url.slice(0, findText);
        // window.open(url,'_blank',);
    },

    _onDownloadAttachment: function(event){
        event.preventDefault();
        var url = event.delegateTarget.dataset['url'];
        window.open(url,'_blank',);
    },

    _onAddAttachment: function (event) {
        var $event = $(event.target);
        // console.log("event----------", event);
        // console.log("$event---------", $event);
        // console.log("$event val---------", $event.val());
        if ($event.val() !== '') {
            var $binaryForm = this.$('form.o_form_binary_form');
            console.log("binaryForm ---------------------2-", $binaryForm);
            console.log("framework ----------------------", framework.blockUI());
            $binaryForm.submit();
            $binaryForm.find('input[type=file]').prop('disabled', true);
            $binaryForm.find('button').prop('disabled', true).find('img, span').toggle();
            this.$('.o_sidebar_add_attachment a').text(_t('Uploading...'));
            framework.blockUI();
        }
    },
    /**
     * Method triggered when user delete an attachment
     *
     * @private
     * @param  {Event} event
     */
    _onDeleteAttachment: function (event) {
        event.preventDefault();
        var self = this;
        var $event = $(event.currentTarget);
        var options = {
            confirm_callback: function () {
                self._rpc({
                    model: 'ir.attachment',
                    method: 'unlink',
                    args: [parseInt($event.attr('data-id'), 10)],
                })
                .then(self._updateAttachments.bind(self))
                .then(self._redraw.bind(self))
                .then(self.getDataSearchRead($event.attr('data-id')));
            }
        };
        Dialog.confirm(this, _t("Bạn có muốn xóa file đính kèm ?"), options);
    },
    getDataSearchRead: function(data){
        console.log("data", data);
        rpc.query({
            model: 'ir.attachment',
            method: 'search_read',
            domain: [["id", "=", data]],
        }).then(function (data_count) {
            console.log("data count1", data_count[0].res_model);
            console.log("data res_id", data_count[0].res_id);

            var model_name = ""+data_count[0].res_model+"" ;
            rpc.query({
                model: model_name,
                method: 'read',
                args: [[data_count[0].res_id]],
            }).then(function(data){
                console.log("dataaaaaaaaaa",data);
            });
        });
    },
    /**
     * Handler called when the upload is done
     *
     * @private
     */
    _onFileUploaded: function () {
        var attachments = Array.prototype.slice.call(arguments, 1);
        var uploadErrors = _.filter(attachments, function (attachment) {
            return attachment.error;
        });
        if (uploadErrors.length) {
            this.do_warn(_t('Uploading Error'), uploadErrors[0].error);
        }
        this._updateAttachments().then(this._redraw.bind(this));
        framework.unblockUI();
    }
});

//chatter.include({
//    start: function () {
//        this._$topbar = this.$('.o_chatter_topbar');
//        if(!this._disableAttachmentBox) {
//            this.$('.o_topbar_right_area').css('display','none');
//        }
//        return this._super.apply(this, arguments);
//    },
//});

mail_act.include({
    start: function () {
        // alert("124")
        $('li:has(a .fa-clock-o)').css('display','none');
        $('.dropdown-divider').css('display','none');
        $('a[data-menu="shortcuts"]').attr('style', 'display: none !important');
        $('a[data-menu="documentation"]').attr('style', 'display: none !important');
        $('a[data-menu="support"]').attr('style', 'display: none !important');
        $('a[data-menu="account"]').attr('style', 'display: none !important');
        return this._super();
    },
});
chatter.include({
    start: function () {
        $(".o_topbar_right_area").attr('disabled', true);
        return this._super.apply(this, arguments);
    },
    _updateMentionSuggestions: function() {
        $(".o_topbar_right_area").css("display","none");
        $(".o_chatter_button_log_note").css("display","none");
        $(".o_chatter_button_new_message").css("display","none");
    }
});
});
odoo.define('preview.WebClient', function (require) {
"use strict";
    var AbstractWebClient = require('web.AbstractWebClient');
    AbstractWebClient = AbstractWebClient.include({
        start: function (parent) {
            this.set('title_part', {"zopenerp": "Công ty Than Na Dương"});
            this._super(parent);
            if($("<a>").text() === 'Thiết lập'){
                $("<a>").css("display","none");
                alert("1");
            }
        },
       
    });
});
