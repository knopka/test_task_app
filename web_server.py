from http.server import HTTPServer, BaseHTTPRequestHandler

def counted(fn):
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return fn(*args, **kwargs)
    wrapper.called = 0
    wrapper.__name__ = fn.__name__
    return wrapper


class S(BaseHTTPRequestHandler):

    count = 0
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @counted   
    def do_POST(self):
        self.count = str(self.do_POST.called)
        self._set_headers()
        S.count = self.count
        self.wfile.write("POST request".encode("utf-8"))
    
    def do_GET(self):
        self._set_headers()
        self.ab = str(S.count)
        self.wfile.write("There were ".encode("utf-8"))
        self.wfile.write(self.ab.encode("utf-8"))
        self.wfile.write(" POST requests".encode("utf-8"))
    

        
def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()
    
if __name__ == '__main__':
	run()
