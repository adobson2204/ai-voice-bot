import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

if not api_key:
    print("Warning: OPENAI_API_KEY not found in environment variables")
    client = None
else:
    client = OpenAI(api_key=api_key)

# Check for required Twilio credentials
if not twilio_account_sid or not twilio_auth_token:
    print("Warning: TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not found in environment variables")


@app.route("/voice", methods=["POST"])
def voice():
    """Handle incoming voice calls"""
    response = VoiceResponse()
    response.say("Hi there. Tell me what you're looking for after the beep.")
    response.record(
        max_length=8,
        action="/process",
        transcribe=True
    )
    return Response(str(response), mimetype="text/xml")


@app.route("/process", methods=["POST"])
def process():
    """Process transcribed audio and generate AI response"""
    transcription = request.form.get("TranscriptionText", "")
    ai_response = "Sorry, I didn't catch that."

    if transcription:
        if not client:
            ai_response = "OpenAI API key is not configured."
        else:
            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": transcription}
                    ]
                )
                ai_response = completion.choices[0].message.content
            except Exception as e:
                print(f"OpenAI API error: {e}")
                ai_response = "I'm having trouble processing your request right now."

    response = VoiceResponse()
    response.say(ai_response)
    return Response(str(response), mimetype="text/xml")


@app.route("/")
def home():
    """Health check endpoint"""
    status = {"app": "Twilio Voice Bot is running!"}

    if not os.getenv("OPENAI_API_KEY"):
        status["openai"] = "ERROR: OPENAI_API_KEY not configured"
    else:
        status["openai"] = "OK"

    if not os.getenv("TWILIO_ACCOUNT_SID") or not os.getenv("TWILIO_AUTH_TOKEN"):
        status["twilio"] = "ERROR: Twilio credentials not configured"
    else:
        status["twilio"] = "OK"

    return status


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
