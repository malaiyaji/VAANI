import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Pulls the secret key you set up in your Render environment variables dashboard!
SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY")

@app.route("/api/voice-incident", methods=["POST"])
def voice_incident():
    # 1. Safeguard check
    if 'file' not in request.files:
        return jsonify({"error": "No audio matrix stream found in payload"}), 400
        
    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify({"error": "Empty audio filename token"}), 400

    try:
        # 2. Forward the binary file stream to Sarvam AI Speech-to-Text
        url = "https://api.sarvam.ai/speech-to-text"
        headers = {
            "api-subscription-key": SARVAM_API_KEY
        }
        
        # Pass the audio stream with its original dynamic filename and content-type
        files = {
            'file': (audio_file.filename, audio_file.read(), audio_file.content_type)
        }
        
        # 🔥 FIX: Changed model to 'saaras:v3' and added the required 'mode' parameter
        data = {
            'model': 'saaras:v3',
            'mode': 'transcribe'
        }

        sarvam_response = requests.post(url, headers=headers, files=files, data=data)
        
        if sarvam_response.status_code != 200:
            print(f"Sarvam AI Error Log: {sarvam_response.text}")
            return jsonify({
                "error": "Sarvam AI Core failed to parse audio token", 
                "details": sarvam_response.text
            }), 502

        # Extract the text transcription returned by Sarvam
        transcript = sarvam_response.json().get("transcript", "")

        # 3. Neural Routing Engine
        text_lower = transcript.lower()
        target_app = "default"
        extracted_params = {}

        if "spotify" in text_lower or "play" in text_lower or "song" in text_lower:
            target_app = "spotify"
            extracted_params["query"] = text_lower.split("play")[-1].strip() if "play" in text_lower else "lofi focus"
            
        elif "youtube" in text_lower or "video" in text_lower:
            target_app = "youtube"
            extracted_params["query"] = text_lower.replace("youtube", "").replace("video", "").strip()
            
        elif "pinterest" in text_lower or "moodboard" in text_lower or "design" in text_lower:
            target_app = "pinterest"
            extracted_params["query"] = text_lower.replace("pinterest", "").strip()
            
        elif "amazon" in text_lower or "buy" in text_lower:
            target_app = "amazon"
            extracted_params["product_query"] = text_lower.replace("amazon", "").replace("buy", "").strip()
            
        elif "eat" in text_lower or "food" in text_lower or "hungry" in text_lower:
            target_app = "food"
            extracted_params["craving"] = "restaurants near me"
            
        elif "note" in text_lower or "write" in text_lower:
            target_app = "notes"
            extracted_params["note_content"] = transcript

        # 4. Success Response
        return jsonify({
            "transcript": transcript,
            "job_id": f"VN-{os.urandom(3).hex().upper()}",
            "incident_type": "NEURAL_COMMAND",
            "sector": "EXEC_GRID_ALPHA",
            "allocated_resource": f"{target_app.upper()}_ROUTER",
            "routing": {
                "target_app": target_app,
                "extracted_params": extracted_params
            }
        })

    except Exception as e:
        print(f"System Pipeline Crash: {str(e)}")
        return jsonify({"error": "Internal Server Exception // 500"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))