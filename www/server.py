import http.server
import socketserver
import threading
import time
import argparse

GET = None


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(str(GET).encode())


parser = argparse.ArgumentParser(
    description="Start a simple GET request server which returns a static string."
)
parser.add_argument("GET", type=str, help="GET Request return value")
parser.add_argument(
    "shutdown_after",
    type=int,
    nargs="?",
    default=600,
    help="Shutdown after __ seconds (default 600 seconds, 10 minutes)",
)
args = parser.parse_args()
GET = args.GET

server = socketserver.TCPServer(("0.0.0.0", 8080), RequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
print(f"Shutdown in {args.shutdown_after}")
time.sleep(args.shutdown_after)
print("Closing server")
server.shutdown()
print("Server closed")
