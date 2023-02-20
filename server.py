from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import socket
import json, time, ast, os

class S(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # for GET
        def respond(opts):
            response = handle_http(opts['status'], self.path)
            self.wfile.write(response)

        # for GET
        def handle_http(status_code, path):
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = '''
            <html><head><title>Title goes here.</title></head>
            <body><p>This is a test.</p>
            <p>You accessed path: {}</p>
            </body></html>
            '''.format(path)
            return bytes(content, 'UTF-8')
        
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            respond(paths[self.path])
        else:
            respond({'status': 500})
        logging.info("\nGET request from %s\nPath: %s\nHeaders:\n%s", str(self.address_string()), str(self.path), str(self.headers))
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        #  body is too long and so is not displayed in log file
        # logging.info("\nPOST request from %s\nPath: %s\nHeaders:\n%s\nBody:\n%s",
        #         str(self.address_string()), str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("\nPOST request from %s\nPath: %s\nHeaders:\n%s\n",
                str(self.address_string()), str(self.path), str(self.headers))

        # send back response to iphone
        self.do_HEAD()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
        # write down the body passed from iphone
        body = ast.literal_eval(post_data.decode('utf-8'))
        # with open(f'frames/{time.strftime("%m-%d %H-%M-%S",time.localtime())}.png', "wb") as f: 
        #     f.write(base64.b64decode(body['image']))
        t = body['dateTime'][0]
        with open(f'frames/{t}.json', "w", encoding='utf8') as f: 
            json.dump(body, f)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    if not os.path.exists('frames/'): 
        os.mkdir('frames') 
    logging.basicConfig(filename='server.log', filemode='w',
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s', level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...{}: {}'.format(socket.gethostbyname(socket.gethostname()), port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()