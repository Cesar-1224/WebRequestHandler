from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def querydata(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):  # Corrección aquí: do_GET
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        if self.path == '/':
            # Leer y enviar el contenido del archivo home.html
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.read_file('home.html').encode('utf-8'))
        else:
            # Manejar rutas no encontradas
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_404_response().encode('utf-8'))

    def read_file(self, filename):
        """Lee el contenido de un archivo dado."""
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "<h1>404 Not Found</h1><p>The requested file was not found.</p>"

    def get_404_response(self):
        """Genera una respuesta HTML para un error 404."""
        return "<h1>404 Not Found</h1><p>The requested URL was not found on this server.</p>"

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()