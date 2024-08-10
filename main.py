from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

hostName = "localhost"
hostPort = 8080

class MiServidor(BaseHTTPRequestHandler):

    def do_GET(self):
        match self.path:
            case "/":
                json_response = requests.get("https://jsonplaceholder.typicode.com/albums")

                if json_response.status_code == 200:
                    # La solicitud fue exitosa
                    json_response = json_response.json()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    for album in json_response:
                        self.wfile.write(
                            bytes(
                                f"<html><body> <h1>{album['title']}</h1> \n Posted by {album['userId']} - Album ID {album['id']} </body></html>", "utf-8"
                            )
                        )
                else:
                    # La solicitud no fue exitosa
                    self.send_response(json_response.status_code)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, hostPort), MiServidor)
    print("Server started http://%s:%s" % (hostName, hostPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")