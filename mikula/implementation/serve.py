import http.server
import socketserver


def serve(gallery, port):

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=gallery, **kwargs)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving on 'http://localhost:{port}'")
        print("Ctrl + C to exit")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\ndone")
