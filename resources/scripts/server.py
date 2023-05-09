def onInput(node):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            from utils.fileLoader import FileLoader
            page = FileLoader.read("resources/scripts/page.html")
            self.wfile.write(page.encode('utf-8'))

        def do_POST(self):
            import urllib
            print(self.headers)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = (post_data.decode('utf-8'))
            # parce data
            data = urllib.parse.parse_qs(data)
            print(data)
            node.stream(data)
            # ここで data を処理する

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = "データが送信されました。"
            self.wfile.write(response.encode('utf-8'))

    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    httpd.serve_forever()
onInput(node)