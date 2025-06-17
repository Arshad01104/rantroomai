import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")
    data = request.get_json()
    prompt = data.get("prompt")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, json=payload)
    result = response.json()

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": text})
    except:
        return jsonify({"error": "Failed", "raw": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
