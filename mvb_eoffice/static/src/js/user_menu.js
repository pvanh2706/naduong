odoo.define('module_folder.ComplementMenu', function(require) {
    "use strict";
    var UserMenu = require('web.UserMenu');
    var ComplementMenu = UserMenu.include({
        _onMenuNewmenu: function () {
         }
      });
    return ComplementMenu;
    });