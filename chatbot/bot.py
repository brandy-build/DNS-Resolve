

import requests
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

def chat(prompt):
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing."
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            # Gemini response parsing
            reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return reply.strip() if reply else "No response from Gemini."
        elif response.status_code == 401:
            return "Error: Unauthorized. Please check your Gemini API key."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        q = input("You: ")
        print("Bot:", chat(q))
