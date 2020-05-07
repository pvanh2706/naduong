odoo.define('theme.snippets.options', function (require) {
'use strict';

var core = require('web.core');
var weWidgets = require('web_editor.widget');
var options = require('web_editor.snippets.options');

var _t = core._t;
var qweb = core.qweb;

options.registry.gallery_multi = options.Class.extend({
    xmlDependencies: ['/theme_company_custom/static/src/xml/theme.gallery.xml'],

    /**
     * @override
     */
    start: function () {
        var self = this;

        // The snippet should not be editable
        this.$target.attr('contentEditable', false);

        // Make sure image previews are updated if images are changed
        this.$target.on('save', 'img', function (ev) {
            var $img = $(ev.currentTarget);
            // var index = self.$target.find('.image-gallery-item.active').index();
            // self.$('.image-gallery:first li[data-target]:eq(' + index + ')')
            //     .css('background-image', 'url(' + $img.attr('src') + ')');
        });

        // When the snippet is empty, an edition button is the default content
        // TODO find a nicer way to do that to have editor style
        this.$target.on('click', '.o_multi_add_images', function (e) {
            e.stopImmediatePropagation();
            self.addImages(false);
        });

        return this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    onBuilt: function () {
        var uuid = new Date().getTime();
        this.$target.find('.image-gallery').attr('id', 'slideshow_' + uuid);
        this.$target.find('[data-target]').attr('data-target', '#slideshow_' + uuid);
    },
    /**
     * @override
     */
    cleanForSave: function () {
        if (this.$target.hasClass('slideshow')) {
            this.$target.removeAttr('style');
        }
    },

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * Allows to select images to add as part of the snippet.
     *
     * @see this.selectClass for parameters
     */
    addImages: function (previewMode) {
        var self = this;
        var $container = this.$('.image-gallery');
        var dialog = new weWidgets.MediaDialog(this, {multiImages: true}, this.$target.closest('.o_editable'), null);
        var lastImage = _.last(this._getImages());
        var index = lastImage ? this._getIndex(lastImage) : -1;
        dialog.on('save', this, function (attachments) {
            for (var i = 0 ; i < attachments.length; i++) {
                $('<img/>', {
                    class: 'img img-fluid',
                    src: attachments[i].src,
                    'data-index': ++index,
                }).appendTo($container);
            }
            self._reset();
            self.trigger_up('cover_update');
        });
        dialog.open();
    },
    /**
     * Allows to change the number of columns when displaying images with a
     * grid-like layout.
     *
     * @see this.selectClass for parameters
     */
    columns: function (previewMode, value) {
        this.$target.attr('data-columns', value);

        var $activeMode = this.$el.find('.active[data-mode]');
        this.mode(null, $activeMode.data('mode'), $activeMode);
    },
    /**
     * Displays the images with the "grid" layout.
     */
    grid: function () {
        var imgs = this._getImages();
        var $row = $('<div/>', {class: 'row'});
        var columns = this._getColumns();
        var colClass = 'col-lg-' + (12 / columns);
        var $container = this._replaceContent($row);

        _.each(imgs, function (img, index) {
            var $img = $(img);
            var $col = $('<div/>', {class: colClass});
            $col.append($img).appendTo($row);
            if ((index + 1) % columns === 0) {
                $row = $('<div/>', {class: 'row'});
                $row.appendTo($container);
            }
        });
        this.$target.css('height', '');
    },
    /**
     * Displays the images with the "masonry" layout.
     */
    masonry: function () {
        var self = this;
        var imgs = this._getImages();
        var columns = this._getColumns();
        var colClass = 'col-lg-' + (12 / columns);
        var cols = [];

        var $row = $('<div/>', {class: 'row'});
        this._replaceContent($row);

        // Create columns
        for (var c = 0; c < columns; c++) {
            var $col = $('<div/>', {class: 'col o_snippet_not_selectable ' + colClass});
            $row.append($col);
            cols.push($col[0]);
        }

        // Dispatch images in columns by always putting the next one in the
        // smallest-height column
        while (imgs.length) {
            var min = Infinity;
            var $lowest;
            _.each(cols, function (col) {
                var $col = $(col);
                var height = $col.is(':empty') ? 0 : $col.find('img').last().offset().top + $col.find('img').last().height() - self.$target.offset().top;
                if (height < min) {
                    min = height;
                    $lowest = $col;
                }
            });
            $lowest.append(imgs.pop());
        }
    },
    /**
     * Allows to change the images layout. @see grid, masonry, nomode, slideshow
     *
     * @see this.selectClass for parameters
     */
    mode: function (previewMode, value, $opt) {
        this.$target.css('height', '');
        this[value]();
        this.$target
            .removeClass('o_nomode o_masonry o_grid o_slideshow')
            .addClass('o_' + value);
    },
    /**
     * Displays the images with the standard layout: floating images.
     */
    nomode: function () {
        var $row = $('<div/>', {class: 'row'});
        var imgs = this._getImages();

        this._replaceContent($row);

        _.each(imgs, function (img) {
            var wrapClass = 'col-lg-3';
            if (img.width >= img.height * 2 || img.width > 600) {
                wrapClass = 'col-lg-6';
            }
            var $wrap = $('<div/>', {class: wrapClass}).append(img);
            $row.append($wrap);
        });
    },
    /**
     * Allows to remove all images. Restores the snippet to the way it was when
     * it was added in the page.
     *
     * @see this.selectClass for parameters
     */
    removeAllImages: function (previewMode) {
        var $addImg = $('<div>', {
            class: 'alert alert-info css_editable_mode_display text-center',
        });
        var $text = $('<span>', {
            class: 'o_multi_add_images',
            style: 'cursor: pointer;',
            text: _t(" Add Images"),
        });
        var $icon = $('<i>', {
            class: ' fa fa-plus-circle',
        });
        this._replaceContent($addImg.append($icon).append($text));
    },
    /**
     * Displays the images with a "slideshow" layout.
     */
    slideshow: function () {
        var imgStyle = this.$el.find('.active[data-styling]').data('styling') || '';
        var urls = _.map(this._getImages(), function (img) {
            return $(img).attr('src');
        });
        var params = {
            srcs : urls,
            // index: 0,
            // title: "",
            // interval : this.$target.data('interval') || false,
            id: 'slideshow_' + new Date().getTime(),
            userStyle: imgStyle,
        },
        $slideshow = $(qweb.render('theme.gallery.slideshow', params));
        this._replaceContent($slideshow);
        // _.each(this.$('img'), function (img, index) {
        //     $(img).attr({contenteditable: true, 'data-index': index});
        // });
        // this.$target.css('height', Math.round(window.innerHeight * 0.7));
        //
        // // Apply layout animation
        // this.$target.off('slide.bs.image-gallery').off('slid.bs.image-gallery');
        // this.$('li.fa').off('click');
        // this._refreshAnimations();
    },
    /**
     * Allows to change the style of the individual images.
     *
     * @see this.selectClass for parameters
     */
    styling: function (previewMode, value) {
        var classes = _.map(this.$el.find('[data-styling]'), function (el) {
            return $(el).data('styling');
        }).join(' ');
        this.$('img').removeClass(classes).addClass(value);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Handles image removals and image index updates.
     *
     * @override
     */
    notify: function (name, data) {
        this._super.apply(this, arguments);
        if (name === 'image_removed') {
            data.$image.remove(); // Force the removal of the image before reset
            this._reset();
        } else if (name === 'image_index_request') {
            var imgs = this._getImages();
            var position = _.indexOf(imgs, data.$image[0]);
            imgs.splice(position, 1);
            switch (data.position) {
                case 'first':
                    imgs.unshift(data.$image[0]);
                    break;
                case 'prev':
                    imgs.splice(position - 1, 0, data.$image[0]);
                    break;
                case 'next':
                    imgs.splice(position + 1, 0, data.$image[0]);
                    break;
                case 'last':
                    imgs.push(data.$image[0]);
                    break;
            }
            _.each(imgs, function (img, index) {
                // Note: there might be more efficient ways to do that but it is
                // more simple this way and allows compatibility with 10.0 where
                // indexes were not the same as positions.
                $(img).attr('data-index', index);
            });
            this._reset();
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Returns the images, sorted by index.
     *
     * @private
     * @returns {DOMElement[]}
     */
    _getImages: function () {
        var imgs = this.$('img').get();
        var self = this;
        imgs.sort(function (a, b) {
            return self._getIndex(a) - self._getIndex(b);
        });
        return imgs;
    },
    /**
     * Returns the index associated to a given image.
     *
     * @private
     * @param {DOMElement} img
     * @returns {integer}
     */
    _getIndex: function (img) {
        return img.dataset.index || 0;
    },
    /**
     * Returns the currently selected column option.
     *
     * @private
     * @returns {integer}
     */
    _getColumns: function () {
        return parseInt(this.$target.attr('data-columns')) || 3;
    },
    /**
     * Empties the container, adds the given content and returns the container.
     *
     * @private
     * @param {jQuery} $content
     * @returns {jQuery} the main container of the snippet
     */
    _replaceContent: function ($content) {
        var $container = this.$('.container:first');
        $container.empty().append($content);
        return $container;
    },
    /**
     * @override
     */
    _setActive: function () {
        this._super();
        var classes = _.uniq((this.$target.attr('class').replace(/(^|\s)o_/g, ' ') || '').split(/\s+/));
        this.$el.find('[data-mode]')
            .removeClass('active')
            .filter('[data-mode="' + classes.join('"], [data-mode="') + '"]').addClass('active');
        var mode = this.$el.find('[data-mode].active').data('mode');

        classes = _.uniq((this.$('img:first').attr('class') || '').split(/\s+/));
        this.$el.find('[data-styling]')
            .removeClass('active')
            .filter('[data-styling="' + classes.join('"], [data-styling="') + '"]').addClass('active');

        this.$el.find('[data-interval]').removeClass('active')
            .filter('[data-interval='+this.$target.find('.image-gallery:first').attr('data-interval')+']')
            .addClass('active');

        var interval = this.$target.find('.image-gallery:first').attr('data-interval');
        this.$el.find('[data-interval]')
            .removeClass('active')
            .filter('[data-interval=' + interval + ']').addClass('active');

        var columns = this._getColumns();
        this.$el.find('[data-columns]')
            .removeClass('active')
            .filter('[data-columns=' + columns + ']').addClass('active');

        this.$el.find('[data-columns]:first, [data-select-class="spc-none"]')
            .parent().parent().toggle(['grid', 'masonry'].indexOf(mode) !== -1);
        this.$el.find('[data-interval]:first').parent().parent().toggle(mode === 'slideshow');
    },
});

options.registry.gallery_multi_img = options.Class.extend({
    /**
     * Rebuilds the whole gallery when one image is removed.
     *
     * @override
     */
    onRemove: function () {
        this.trigger_up('option_update', {
            optionName: 'gallery',
            name: 'image_removed',
            data: {
                $image: this.$target,
            },
        });
    },

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * Allows to change the position of an image (its order in the image set).
     *
     * @see this.selectClass for parameters
     */
    position: function (previewMode, value) {
        this.trigger_up('deactivate_snippet');
        this.trigger_up('option_update', {
            optionName: 'gallery',
            name: 'image_index_request',
            data: {
                $image: this.$target,
                position: value,
            },
        });
    },
});
});
