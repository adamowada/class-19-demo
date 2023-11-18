from chatgpt.summarizer import article_summary
from web_scraper.ap_scraper import scraper

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Take the url query string and create a dictionary of parameters
        url = self.path
        url_components = parse.urlsplit(url)
        query_string_list = parse.parse_qsl(url_components.query)
        dictionary = dict(query_string_list)  # /?news=something

        # We can do stuff!
        print(dictionary)
        if dictionary.get("news"):
            raw_story = scraper(dictionary.get("news"))
            summary = f"{raw_story[0]}\n\n{article_summary(raw_story[1])}"
        else:
            summary = "No query string found."

        # forming the response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(summary.encode())


if __name__ == '__main__':
    # http://localhost:8000/?news=cars
    server_address = ('localhost', 8000)  # use any available port
    httpd = HTTPServer(server_address, handler)  # httpd is a commonly used abbreviation for "HTTP Daemon"
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
