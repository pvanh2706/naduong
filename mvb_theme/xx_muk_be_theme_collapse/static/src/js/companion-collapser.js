odoo.define('xx_muk_be_theme_collapse.collapse_button', function (require) {
"use strict";

$(document).ready(function() {

    $("div#mwt_companion_collapser").click(function(e) {
    	e.stopPropagation();
        e.preventDefault();
        
        // Left menu
        var $mk_apps_sidebar_panel = $(".mk_apps_sidebar_panel");

        // Get padding of main content
        var get_padding = $(".o_main_content").innerWidth() - $(".o_main_content").width();
    	var sidebar_panel_width = $mk_apps_sidebar_panel.width();

    	$("#mwt_companion_collapser > .companion-collapser-button").toggleClass("companion-collapser-button-checked");

        $mk_apps_sidebar_panel.animate({
            width: ['toggle', 'swing'],
            opacity: 'toggle'
        }, 150, 'linear');

        $(".o_main_content").animate({
            'padding-left': get_padding ? 0 : sidebar_panel_width,
        }, 150, 'linear');
    });
});
});
