import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenWebUI API URL
VAST_AI_URL = "https://70.48.62.199:43678/api"

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask API! Use the /process endpoint to interact with the model.", 200

# /process endpoint
@app.route('/process', methods=['POST'])
def process_request():
    try:
        # Log incoming request
        data = request.json
        print(f"Received data: {data}")

        # Include the Authorization header with the API key
        headers = {
            "Authorization": "Bearer sk-1129fd65894e45eca4ecf6924b06b139",
            "Content-Type": "application/json"
        }

        # Forward the request to OpenWebUI
        print(f"Forwarding request to OpenWebUI: {VAST_AI_URL} with data {data}")
        response = requests.post(VAST_AI_URL, json=data, headers=headers, timeout=10, verify=False)

        # Log OpenWebUI response
        print(f"OpenWebUI response status: {response.status_code}")
        print(f"OpenWebUI response: {response.text}")

        # Handle non-successful HTTP responses
        response.raise_for_status()

        # Return the successful response to the client
        return jsonify(response.json()), 200

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from OpenWebUI: {e}")
        return jsonify({"error": "HTTP error while communicating with OpenWebUI", "details": str(e)}), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Request error communicating with OpenWebUI: {e}")
        return jsonify({"error": "Request error communicating with OpenWebUI", "details": str(e)}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on all network interfaces, listening on port 8081
    app.run(host='0.0.0.0', port=8081)
