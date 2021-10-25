from http.server import BaseHTTPRequestHandler, HTTPServer
import gitbot_function, gitbot_module, json, configparser, logging
import argparse, sys

class Webhook(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        eventType = json.loads(post_data)['type']
        resource = json.loads(post_data)['event_data']['resources'][0]['resource_url']
        if eventType == "PUSH_ARTIFACT": 
        # if eventType == "pushImage": 
            logging.info("-"*100)
            logging.info("GitBot is proceeding...")
            gitbot_function.gitBot(resource, configPath, binPath)
            
def run(server_class=HTTPServer, handler_class=Webhook, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    logging.info("="*100)
    logging.info("Starting Webhook endpoint on {}:{}".format(addr, port))
    httpd.serve_forever()

if __name__ == "__main__":
    # Gitbot help menu
    parser = argparse.ArgumentParser(description="Webhook endpoint for Gitlab-ci")
    parser.add_argument('-i', metavar='IP_ADDRESS', nargs=1, type=str, help='Listening IP Address')
    parser.add_argument('-p', metavar='PORT', nargs=1, type=int, help='Listening Port')
    parser.add_argument('-c', metavar='CONFIG_FILE', nargs=1, type=str, help='Config File')
    args = parser.parse_args()
    if len(sys.argv) > 1: configPath = args.c[0]; binPath = '/'.join(args.c[0].split('/')[:-1])
    else: parser.print_help()

    # Config file module
    parser = configparser.ConfigParser()
    parser.read(configPath)

    # Logging module
    gitbot_module.logConfig(parser)

    # Variable definition                
    endpointAddress = parser.get('ENDPOINT', 'ENDPOINT_ADDRESS')
    endpointPort = parser.get('ENDPOINT', 'ENDPOINT_PORT')

    # Webhook run
    run(addr=endpointAddress, port=int(endpointPort))