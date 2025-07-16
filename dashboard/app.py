from flask import Flask, render_template, request, jsonify
from resolver.resolver import resolve
import os
from dotenv import load_dotenv
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chatbot')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot.bot import chat

# Supabase setup
from supabase import create_client, Client
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rfqywkxmxvovdhfijwhw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJmcXl3a3hteHZvdmRoZmlqd2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjY2MjY3MCwiZXhwIjoyMDY4MjM4NjcwfQ.GzmFMEAyQWVWY_InwkmfsxdpkxuSMeQpna5xGhkcweU")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    chat_reply = None
    domain = None
    user_message = None
    if request.method == "POST":
        if "domain" in request.form:
            domain = request.form["domain"]
            result = resolve(domain)
            # Log DNS query to Supabase
            try:
                supabase.table("dns_logs").insert({"domain": domain, "result": str(result)}).execute()
            except Exception as e:
                print("Supabase DNS log error:", e)
        if "user_message" in request.form:
            user_message = request.form["user_message"]
            chat_reply = chat(user_message)
            # Log chatbot query to Supabase
            try:
                supabase.table("chatbot_logs").insert({"user_message": user_message, "chat_reply": chat_reply}).execute()
            except Exception as e:
                print("Supabase Chatbot log error:", e)
    return render_template("index.html", result=result, domain=domain, chat_reply=chat_reply, user_message=user_message)

@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    user_message = request.json.get("user_message", "")
    chat_reply = chat(user_message)
    # Log chatbot query to Supabase
    try:
        supabase.table("chatbot_logs").insert({"user_message": user_message, "chat_reply": chat_reply}).execute()
    except Exception as e:
        print("Supabase Chatbot log error:", e)
    return jsonify({"reply": chat_reply})

if __name__ == "__main__":

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)