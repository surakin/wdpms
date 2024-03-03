#!/usr/bin/env python3

import pywayland
import pywayland.client
import protocols.wayland
import protocols.dpms
import argparse
import sys

output = []

def _get_registry_callback(registry, id, iface_name, version):
    global dpms_manager, output
    if iface_name == "org_kde_kwin_dpms_manager":
        dpms_manager = registry.bind(id, protocols.dpms.OrgKdeKwinDpmsManager, version)
    elif iface_name == "wl_output":
        output.append(registry.bind(id, protocols.wayland.WlOutput, version))


def get_dpms_state():
    dpms_mode = 0
    def _get_mode_callback(_, m):
        dpms_mode = m
    with pywayland.client.Display() as display:
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
    return dpms_mode

def set_dpms_state(state):
    with pywayland.client.Display() as display:
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

parser = argparse.ArgumentParser(prog='dpms', description='Wayland DPMS tool')
parser.add_argument('-q', '--query', action='store_true', help='Get DPMS state')
parser.add_argument('--on', action='store_true', help='Turn on display(s)')
parser.add_argument('--off', action='store_true', help='Turn off display(s)')
args = parser.parse_args()

if args.query:
    state = get_dpms_state()
    print(state)
    #sys.exit(0 if state == 3 else 1)
elif args.on:
    set_dpms_state(True)
elif args.off:
    set_dpms_state(False)