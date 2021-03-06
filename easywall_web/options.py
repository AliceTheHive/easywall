"""the module contains functions for the options route"""
from flask import render_template, request
from easywall_web.login import login
from easywall_web.webutils import Webutils


def options(saved=False):
    """the function returns the options page when the user is logged in"""
    utils = Webutils()
    if utils.check_login(request) is True:
        payload = utils.get_default_payload("Options")
        payload.config = utils.cfg_easywall
        payload.saved = saved
        return render_template('options.html', vars=payload)
    return login("", None)


def options_save():
    """
    the function saves the options from a section using the config class
    for example the Enabled flag in the IPv6 section is saved to the config file
    """
    utils = Webutils()
    if utils.check_login(request) is True:
        section = request.form['section']
        for key, value in request.form.items():
            if key != "section":
                if key.startswith("checkbox"):
                    key = key.replace("checkbox_", "")
                    value = correct_value_checkbox(key)
                if value != "on":
                    utils.cfg_easywall.set_value(section, key, value)
        return options(True)
    return login("", None)


def correct_value_checkbox(key):
    """the function corrects the value of a checkbox"""
    key = key.replace("checkbox_", "")
    if key in request.form:
        return "yes"
    return "no"
