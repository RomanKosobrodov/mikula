import http.server
import socketserver


def serve(gallery, port):

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=gallery, **kwargs)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()
