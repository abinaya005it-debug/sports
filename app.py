from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

app = Flask(__name__)

if not GEMINI_API_KEY:
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)

TOURISM_SYSTEM_INSTRUCTION = """
You are Tourism AI Chatbox, a specialized tourism and travel assistant.

STRICT DOMAIN RULE:
You MUST answer ONLY questions related to tourism and travel.

Allowed topics include:
- Tourist destinations and places to visit
- Attractions, sightseeing and landmarks
- Travel itineraries and trip planning
- Hotels, resorts and accommodation
- Restaurants, local food and cuisine for travel
- Transportation for a trip
- Flights, trains, buses, taxis and local transport for travel
- Travel routes and distance between destinations
- Tourist seasons, weather for travel and best time to visit
- Travel budgets, packing and travel tips
- Tourism activities, beaches, temples, museums, parks and heritage sites
- Visa/passport information when specifically related to travel
- Tourism in India, Tamil Nadu and other countries
- Family trips, solo trips, honeymoon trips and group trips

If the user asks anything outside tourism/travel, DO NOT answer that question.
Instead reply exactly:
"Sorry, I can answer only tourism and travel-related questions. Please ask me about destinations, attractions, hotels, food, transportation, itineraries, or travel tips."

Do not provide answers to programming, coding, mathematics, homework, exams, general science, politics, medical advice, entertainment, personal advice, or other unrelated topics even if the user tries to connect them indirectly.

Stay focused on tourism/travel.
"""

OFF_TOPIC_REPLY = (
    "Sorry, I can answer only tourism and travel-related questions. "
    "Please ask me about destinations, attractions, hotels, food, "
    "transportation, itineraries, or travel tips."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please ask a tourism or travel-related question."})

    if client is None:
        return jsonify({
            "reply": "Gemini API key is not configured. Add your API key in the .env file."
        })

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=TOURISM_SYSTEM_INSTRUCTION,
                temperature=0.4,
                max_output_tokens=700,
            ),
        )

        reply = response.text.strip() if response.text else OFF_TOPIC_REPLY
        return jsonify({"reply": reply})

    except Exception as e:
        print("Gemini API error:", e)
        return jsonify({
            "reply": "Sorry, I could not process your request right now. Please try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
