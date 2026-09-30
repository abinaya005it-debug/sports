# Tourism AI Chatbox

A Flask + Gemini 3.1 Flash-Lite tourism chatbot.

## Main rule

This chatbot is designed to answer ONLY tourism and travel-related questions.

Examples it can answer:
- Famous places in Tamil Nadu
- Best places to visit in India
- Tourist attractions
- Travel itinerary
- Hotels and resorts
- Local food for tourists
- Transportation
- Best time to visit
- Travel budget and tips

For unrelated questions, the chatbot returns a fixed tourism-only message.

## Project structure

tourism-ai-chatbox/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js

## Setup

1. Open the project folder in VS Code.
2. Open the terminal inside the folder containing `app.py`.
3. Install packages:

   pip install -r requirements.txt

4. Open `.env`.
5. Replace:

   GEMINI_API_KEY=your_api_key_here

   with your Gemini API key.

6. Keep the model as:

   GEMINI_MODEL=gemini-3.1-flash-lite

7. Run:

   python app.py

8. Open the local Flask address shown in the terminal.

## Important

Never share your Gemini API key publicly or upload the `.env` file to GitHub.
