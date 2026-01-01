/** @odoo-module **/

import { Component } from "@odoo/owl";

export class WidgetAnnouncement extends Component {
    static props = {
        userIsAdmin: Boolean,
        announcement: String,
        onChangeAnnouncement: Function,
        onSaveAnnouncement: Function,
    };
    static template = "zehntech_main_menu.WidgetAnnouncement";
}
