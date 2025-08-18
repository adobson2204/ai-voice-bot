
import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    return str(response)

@app.route("/process", methods=["POST"])
def process():
    """Process transcribed audio and generate AI response"""
    transcription = request.form.get("TranscriptionText", "")
    ai_response = "Sorry, I didn't catch that."

    if transcription:
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
    return str(response)

@app.route("/")
def home():
    """Health check endpoint"""
    return "Twilio Voice Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
