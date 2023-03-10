#!/usr/bin/env python3
from flask import Flask, request, render_template
from urllib.parse import urlparse
import requests
import tldextract
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    url = request.args.get('url')
    if url:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            if url.startswith("http:///"):
                url = "http://" + url[len("http:///"):]
            else:
                url = "http://" + url
        if not parsed_url.netloc:
            if url.startswith("http:///"):
                url = url.replace("http:///", "http://")
            elif url.startswith("https:///"):
                url = url.replace("https:///", "https:///")
        extracted = tldextract.extract(url)
        if extracted.suffix:
            domain = extracted.registered_domain
            try:
                ip = str(ipaddress.ip_address(domain))
                url = url.replace(domain, ip)
            except ValueError:
                pass
        response = requests.get(url)
        return render_template('index.html', response_text=response.text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)