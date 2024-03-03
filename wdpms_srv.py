#!/usr/bin/env python3

import argparse
import http.server
import urllib.parse
import json
import wdpms

class WDPMSHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if url.query == 'state':
            state = wdpms.get_dpms_state()
            response = {"dpms": 'false' if state == 3 else 'true' }
            self.wfile.write(json.dumps(response).encode())
            #self.wfile.write(b'hola')

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if url.query == "on":
            wdpms.set_dpms_state(True)
        elif url.query == "off":
            wdpms.set_dpms_state(False)
        elif url.query == "state":
            content_length = int(self.headers['Content-Length'])
            state = json.loads(self.rfile.read(content_length))
            if 'dpms' in state:
                if state['dpms'] == "on":
                    wdpms.set_dpms_state(True)
                elif state['dpms'] == "off":
                    wdpms.set_dpms_state(False)
            print(state)


class WDPMSServer(http.server.HTTPServer):
    def __init__(self, server_address):
        super().__init__(server_address, WDPMSHandler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='wdpms_srv', description='WDPMS http server')
    parser.add_argument('-p', '--port', default=8000, help='port', type=int)
    args = parser.parse_args()

    try:
        with WDPMSServer(server_address=('',args.port)) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass

