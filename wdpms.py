#!/usr/bin/env python3

import argparse
import subprocess
import re

import pywayland
import pywayland.client
import protocols.wayland
import protocols.dpms

output = []
dpms_manager = None
dpms_mode = 0

def _get_registry_callback(registry, id, iface_name, version) -> None:
    if iface_name == "org_kde_kwin_dpms_manager":
        global dpms_manager
        dpms_manager = registry.bind(id, protocols.dpms.OrgKdeKwinDpmsManager, version)
    elif iface_name == "wl_output":
        global output
        output.append(registry.bind(id, protocols.wayland.WlOutput, version))


def get_dpms_state() -> None:
    global output
    global dpms_mode
    def _get_mode_callback(_, m):
        global dpms_mode
        dpms_mode = m
    try:
        with pywayland.client.Display() as display:
            output = []
            display.connect()
            registry = display.get_registry()
            registry.dispatcher["global"] = _get_registry_callback
            display.dispatch(block=True)
            display.sync()

            dpms = []
            for i in output:
                dpms.append(dpms_manager.get(i))

            for i in dpms:
                i.dispatcher["mode"] = _get_mode_callback

            display.dispatch(block=True)
    except ValueError:
        dpms = subprocess.check_output(['xset', '-q']).decode()
        m1 = re.search('.*DPMS is (.*)', dpms)
        m2 = re.search('.*Monitor is (.*)', dpms)
        if m2:
            dpms_mode = 3 if m2[1] == 'Off' else 0
        elif m1:
            dpms_mode = 0 if m1[1] == 'Enabled' else 3
    return dpms_mode

def set_dpms_state(state) -> None:
    global output
    try:
        with pywayland.client.Display() as display:
            output = []
            display.connect()
            registry = display.get_registry()
            registry.dispatcher["global"] = _get_registry_callback
            display.dispatch(block=True)
            display.sync()

            dpms = []
            for i in output:
                dpms.append(dpms_manager.get(i))
            for i in dpms:
                i.set(0 if state else 3)
            display.dispatch(block=True)
    except ValueError:
        subprocess.check_call(['xset', 'dpms', 'force', 'on' if state == 1 else 'off'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='dpms', description='Wayland DPMS tool')
    parser.add_argument('-q', '--query', action='store_true', help='Get DPMS state')
    parser.add_argument('--on', action='store_true', help='Turn on display(s)')
    parser.add_argument('--off', action='store_true', help='Turn off display(s)')
    args = parser.parse_args()

    if args.query:
        state = get_dpms_state()
        #sys.exit(0 if state == 3 else 1)
    elif args.on:
        set_dpms_state(True)
    elif args.off:
        set_dpms_state(False)
