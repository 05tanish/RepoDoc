import http.server
import socketserver
import threading
import os
import webbrowser

class ReportHandler(http.server.SimpleHTTPRequestHandler):
    report_html = "<h1>Running...</h1>"

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(ReportHandler.report_html.encode('utf-8', 'ignore'))
        else:
            super().do_GET()

def start_server(port: int = 8080):
    """Starts the web server in a background thread."""
    handler = ReportHandler
    try:
        httpd = socketserver.TCPServer(("", port), handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"\\n🌐 Live Dashboard running at http://localhost:{port}")
        # Try to open browser
        try:
            webbrowser.open(f"http://localhost:{port}")
        except:
            pass
        return httpd
    except Exception as e:
        print(f"Server Error: {e}")
        return None
