from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from geocode.api import geocode

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	#Overriding the built in get..
	def do_GET(self):
		try:
			if self.path.startswith('/geocode/resolve/'):
				address = self.path.split('/geocode/resolve/')[1]
				output = json.dumps(geocode(address))
			else:
				with open('geocode/templates/geocode/docs.html', 'r') as f:
					output = f.read()
		except:
			self.send_response(500)
			self.end_headers()
			self.wfile.write("Something went wrong, its possible that your url might be malformed.")
			return
		self.send_response(200)
		self.end_headers()
		self.wfile.write(bytes(output))

if __name__ == "__main__":
	httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
	httpd.serve_forever()
