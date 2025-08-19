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

@app.route("/process", methods=["POST"])
def process():
    """Process transcribed audio and generate AI response"""
    print("----- Incoming POST from Twilio -----", file=sys.stderr)
    print(request.form, file=sys.stderr)  # Logs everything Twilio sends
    print("-------------------------------------", file=sys.stderr)

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
    return str(response

