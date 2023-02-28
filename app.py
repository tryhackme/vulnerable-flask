#!/usr/bin/env python
from flask import Flask, request, render_template
from urllib.parse import urlparse
import requests
import tldextract

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
        if not extracted.suffix:
            if "." not in extracted.domain:
                extracted = extracted._replace(domain=extracted.domain + ".com")
            url = extracted.registered_domain
            response = requests.get(url)
            return render_template('index.html', response_text=response.text)
        response = requests.get(url)
        return render_template('index.html', response_text=response.text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=80, debug=False)