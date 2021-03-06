"""the module contains functions for the ports route"""
from flask import render_template, request
from easywall_web.login import login
from easywall_web.webutils import Webutils
from easywall.rules_handler import RulesHandler


def ports(saved=False):
    """the function returns the ports page when the user is logged in"""
    utils = Webutils()
    rules = RulesHandler()
    if utils.check_login(request) is True:
        payload = utils.get_default_payload("Ports")
        payload.tcp = rules.get_rules_for_web("tcp")
        payload.udp = rules.get_rules_for_web("udp")
        payload.custom = False
        if rules.diff_new_current("tcp") is True or rules.diff_new_current("udp") is True:
            payload.custom = True
        payload.saved = saved
        return render_template('ports.html', vars=payload)
    return login("", None)


def ports_save():
    """the function saves the tcp and udp rules into the corresponding rulesfiles"""
    utils = Webutils()
    if utils.check_login(request) is True:
        action = "add"
        ruletype = "tcp"
        port = ""

        for key, value in request.form.items():
            if key == "remove":
                action = "remove"
                ruletype = value
            elif key == "tcpudp":
                action = "add"
                ruletype = value
            elif key == "port":
                port = str(value)
            else:
                port = str(key)

        if action == "add":
            add_port(port, ruletype)
        else:
            remove_port(port, ruletype)

        return ports(True)
    return login("", None)


def add_port(port, ruletype):
    """the function adds a port to the opened port rules file"""
    rules = RulesHandler()
    rulelist = rules.get_rules_for_web(ruletype)
    rulelist.append(port)
    rules.save_new_rules(ruletype, rulelist)


def remove_port(port, ruletype):
    """the function removes a port from the opened port rules file"""
    rules = RulesHandler()
    rulelist = rules.get_rules_for_web(ruletype)
    rulelist.remove(port)
    rules.save_new_rules(ruletype, rulelist)
