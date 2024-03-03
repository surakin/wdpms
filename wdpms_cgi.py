#!/usr/bin/env python3

import os
import wdpms

print('Content-type: text/html\r\n')

query = os.getenv('QUERY_STRING')
if query == 'state':
    print(wdpms.get_dpms_state())
elif query == 'on':
    wdpms.set_dpms_state(True)
elif query == 'off':
    wdpms.set_dpms_state(False)
