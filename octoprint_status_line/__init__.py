# coding=utf-8
from __future__ import absolute_import

import flask

import octoprint.plugin

class StatusLine(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.SimpleApiPlugin,
                       octoprint.plugin.OctoPrintPlugin
                       ):

    def __init__(self):
        self.message = ""

    # OctoPrintPlugin hook

    def hook_m117(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode and gcode == "M117":
            self._logger.debug("Sent M117 command: {0}".format(cmd))
            self.message = [cmd[5:], self.message.split("\n")][:30]
            self._plugin_manager.send_plugin_message(self._identifier, dict(status_line=self.message))

    # AssetPlugin

    def get_assets(self):
        return {
            "js": ["js/status_line.js"]
        }

    # TemplatePlugin

    def get_template_configs(self):
        return [
            dict(type="sidebar", name="M117 History", icon="comment")
        ]

    # SimpleApiPlugin

    def on_api_get(self, request):
        return flask.jsonify(dict(
            status_line=self.message
        ))

__plugin_name__ = "OctoPrint-StatusLine"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = StatusLine()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.hook_m117
    }

