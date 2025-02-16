from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Vast.ai OpenWebUI API URL and API Key
VAST_AI_URL = "https://70.48.62.199:43678/api"
API_KEY = "de54e0ef7c4a3ea325c0f7c6f71660a541dbbfeb03208d4d8307d0b275b297ea"

# Default route for root ('/') to avoid 404 or 405 errors
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Flask Backend. Use the /query endpoint to interact."

# Route for handling /query endpoint
@app.route("/query", methods=["POST"])
def query_llm():
    user_input = request.json.get("input")
    if not user_input:
        return jsonify({"error": "Input is required"}), 400

    # Prepare payload and headers for the Vast.ai API
    payload = {"input": user_input}
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        # Log outgoing request
        print(f"Sending request to Vast.ai API: {VAST_AI_URL}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")

        # Send request to the Vast.ai API
        response = requests.post(VAST_AI_URL, json=payload, headers=headers, verify=False)

        # Log response details
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        # Raise an error if the response status is not successful
        response.raise_for_status()

        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"error": f"HTTP error: {response.status_code}"}), 500
    except Exception as e:
        print(f"Other error occurred: {e}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

# Route for favicon.ico requests to avoid unnecessary logs
@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
