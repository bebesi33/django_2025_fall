from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 7000


DIRECTORY = (
    r"D:\programming\WebProg2025Fall\webprog_2025_fall\django_2025_fall\lecture_01\f1_b"
)


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


handler = CustomHandler


with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
