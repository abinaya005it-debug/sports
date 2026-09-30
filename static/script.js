from flask import Flask, render_template, request, jsonify
from config import GEMINI_API_KEY
from google import genai
from google.genai import types

app = Flask(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are SportsBot, a chatbot strictly limited to the SPORTS domain.

You may answer ONLY questions related to sports, such as:
- Football, cricket, basketball, tennis, volleyball, badminton, hockey, baseball, athletics, Olympics, etc.
- Players, teams, coaches, tournaments, rules, records, scores, schedules, techniques, sports history and sports training.
- Sports-related explanations and general sports knowledge.

If the user's question is NOT related to sports, do not answer it.
Reply exactly:
"Sorry, I can answer sports-related questions only."

Do not provide answers to programming, education, mathematics, science, politics, entertainment, cooking, health, or other non-sports topics.

Keep answers clear and helpful.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"answer": "Please enter a sports-related question."})

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
            ),
        )
        answer = response.text or "Sorry, I could not generate an answer."
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
