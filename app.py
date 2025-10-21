import os
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Serve main page etc
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/privacy.html")
def privacy():
    return send_from_directory(".", "privacy.html")

@app.route("/about.html")
def about():
    return send_from_directory(".", "about.html")

@app.route("/contact.html")
def contact():
    return send_from_directory(".", "contact.html")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route("/examples.html")
def examples():
    return send_from_directory(".", "examples.html")

# Handle AI-powered rant response
@app.route("/rant", methods=["POST"])
def handle_rant():
    data = request.get_json()
    rant = data.get("rant", "")
    tone = data.get("tone", "")

    prompts = {
        "best_friend": f"As your best friend, I just heard your rant: '{rant}'. Here's my supportive and fun reply:",
        "savage": f"Roast this person mercilessly for saying: '{rant}'",
        "zen_monk": f"Answer with peace and wisdom like a monk to this rant: '{rant}'",
        "therapist": f"As a therapist, gently respond to this rant: '{rant}'",
        "teacher": f"As a strict but caring school teacher, reply to this student rant: '{rant}'",
        "reporter": f"Report this rant like breaking news on live TV: '{rant}'"
    }

    prompt = prompts.get(tone, f"Reply to this rant: '{rant}'")

    # Use Gemini 2.0 Flash Experimental API endpoint
    url = ("https://generativelanguage.googleapis.com/v1beta/"
           "models/gemini-2.0-flash-exp:generateContent?key=" + GEMINI_API_KEY)

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        # You can optionally add generationConfig for temperature, etc
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 256
        }
    }

    response = requests.post(url, json=payload)
    result = response.json()

    try:
        # The response format: candidates → content → parts → text
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({
            "reply": "❌ Gemini could not process the request.",
            "error": result,
            "exception": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))