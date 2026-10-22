from datetime import datetime
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# The API key stays on the Python server, never in browser JavaScript.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


def answer_with_ai(question):
    """Send a general question to Gemini and return its text answer."""
    if not GEMINI_API_KEY:
        return (
            "AI answering is not set up yet. Set the GEMINI_API_KEY "
            "environment variable and restart JARVIS."
        )

    payload = {
        "systemInstruction": {
            "parts": [{
                "text": (
                    "You are JARVIS, a helpful voice assistant. Answer in two or three complete, beginner-friendly sentences. Finish each thought before stopping. "
                    "Say when you "
                    "are unsure."
                )
            }]
        },
        "contents": [{"parts": [{"text": question}]}],
        "generationConfig": {
            "maxOutputTokens": 350,
            "temperature": 0.7,
        },
    }
    request_to_ai = Request(
        GEMINI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        method="POST",
    )

    try:
        with urlopen(request_to_ai, timeout=20) as result:
            result_data = json.loads(result.read().decode("utf-8"))

        parts = result_data.get("candidates", [{}])[0].get(
            "content", {}
        ).get("parts", [])
        answer = " ".join(
            part.get("text", "") for part in parts
        ).strip()
        return answer or "I couldn't create an answer. Please try again."
    except HTTPError as error:
        # Keep API keys and provider error details out of the response to the website.
        app.logger.warning("Gemini returned HTTP status %s", error.code)
        if error.code in (401, 403):
            return "I couldn't access the AI service. Please check the API key."
        if error.code == 429:
            return "The AI service is busy. Please try again shortly."
        return "The AI service had a problem. Please try again shortly."
    except (TimeoutError, URLError):
        return "I couldn't reach the AI service. Please check your internet connection."
    except (KeyError, IndexError, TypeError, ValueError):
        app.logger.warning("Gemini returned an unexpected response format")
        return "I couldn't read the AI answer. Please try again."


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "JARVIS Python backend is running!"
    })


@app.route("/command", methods=["POST"])
def process_command():
    data = request.get_json(silent=True) or {}
    command = data.get("command", "").strip().lower()

    if not command:
        return jsonify({"response": "Please enter a command."}), 400

    # Keep the existing commands local, quick, and usable without an API key.
    if "hello" in command or "hi jarvis" in command:
        response = "Hello! I am JARVIS. How can I help you?"
    elif "joke" in command:
        response = "Why do programmers prefer dark mode? Because light attracts bugs!"
    elif "who are you" in command or "your name" in command:
        response = "I am JARVIS, your personal voice assistant."
    elif "what can you do" in command or "your features" in command:
        response = "I can tell you the time and date, tell jokes, answer greetings, and help you search the web."
    elif "thank you" in command or "thanks" in command:
        response = "You're welcome! I'm always ready to help."
    elif "good morning" in command:
        response = "Good morning! I hope you have a productive day."
    elif "good night" in command:
        response = "Good night! Have a wonderful rest."
    elif "time" in command:
        response = f"The current time is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in command:
        response = f"Today's date is {datetime.now().strftime('%d %B %Y')}."
    else:
        # Questions not matched above are answered by Gemini.
        response = answer_with_ai(command)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)




