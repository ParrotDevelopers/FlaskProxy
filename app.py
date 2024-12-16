from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream():
    # Get the URL argument
    url = request.args.get('url')
    if not url:
        return "URL parameter is required", 400

    # Make the request to the external URL with stream=True
    try:
        with requests.get(url, stream=True) as r:
            # Check if the request was successful
            if r.status_code != 200:
                return f"Failed to fetch {url}: {r.status_code}", r.status_code
            
            # Get the content type from the response
            content_type = r.headers.get('Content-Type', 'application/octet-stream')

            # Return the content as a stream, preserving the content type
            return Response(r.iter_content(chunk_size=1024), content_type=content_type)
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}", 500

@app.route('/standard', methods=['GET'])
def standard():
    # Get the URL argument
    url = request.args.get('url')
    if not url:
        return "URL parameter is required", 400

    # Make the request to the external URL
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return f"Failed to fetch {url}: {r.status_code}", r.status_code
        
        # Get the content type from the response
        content_type = r.headers.get('Content-Type', 'application/octet-stream')

        # Return the content as a stream, preserving the content type
        return Response(r.content, content_type=content_type)
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}", 500


