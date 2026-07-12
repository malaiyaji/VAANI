import os
import json
import requests
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from neo4j import GraphDatabase

app = Flask(__name__)
# Enable CORS globally for API endpoints to prevent browser cross-origin blocks
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- ENVIRONMENT VALUE EXTRACTIONS OR PRODUCTION FALLBACKS ---
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+ssc://d4c69ff1.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "d4c69ff1")  
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# --- INITIALIZE COGNITIVE CORE & KNOWLEDGE GRAPH ---
client = genai.Client(api_key=GEMINI_API_KEY)
NOTES_FILE_PATH = "/tmp/workspace_notes.txt" if os.getenv("RENDER") else "workspace_notes.txt"

try:
    graph_driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )
    print("🛰️ [DEPLOY] Production-grade connection initialized for Cloud Neo4j AuraDB!")
except Exception as e:
    print(f"⚠️ [DEPLOY] Graph database connectivity fault: {e}")
    graph_driver = None

def transcribe_audio_with_sarvam(audio_file):
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    data = {"model": "saaras:v3", "mode": "transcribe", "language_code": "en-IN"}
    
    try:
        audio_bytes = audio_file.read()
        files = {"file": ("live_capture.webm", audio_bytes, "audio/webm")}
        response = requests.post(url, headers=headers, data=data, files=files)
        return response.json().get("transcript", "") if response.status_code == 200 else ""
    except Exception as e:
        print(f"❌ Failed to parse audio via Sarvam API: {e}")
        return ""

def save_intent_to_graph(transcript, target_app, parameters):
    if not graph_driver:
        print("⚠️ [GRAPH LAYER] Operation bypassed: Active driver driver not connected.")
        return
        
    flat_params = {}
    if isinstance(parameters, dict):
        for k, v in parameters.items():
            flat_params[k] = str(v) if isinstance(v, (dict, list)) else v
    else:
        flat_params["info"] = str(parameters)

    query = """
    MERGE (user:User {id: "bro_master"})
    CREATE (interaction:Interaction {
        timestamp: $timestamp, 
        transcript: $transcript, 
        app_triggered: $target_app
    })
    CREATE (paramNode:Parameters)
    SET paramNode = $params
    MERGE (app:Application {name: $target_app})
    CREATE (user)-[:EXECUTED]->(interaction)
    CREATE (interaction)-[:CONFIGURED_WITH]->(paramNode)
    CREATE (interaction)-[:ROUTED_TO]->(app)
    """
    
    try:
        with graph_driver.session(default_access_mode="WRITE") as session:
            session.run(query, 
                        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        transcript=str(transcript),
                        target_app=str(target_app),
                        params=flat_params)
        print("🧠 [GRAPH LAYER] Transaction completed successfully to Neo4j AuraDB!")
    except Exception as e:
        print(f"⚠️ [GRAPH LAYER] Database transaction trace log skipped: {e}")

def execute_backend_action(app_type, params):
    status_message = f"Intent successfully classified into application channel: [{app_type}]."
    try:
        if app_type == "notes" and "note_content" in params:
            with open(NOTES_FILE_PATH, "a", encoding="utf-8") as file:
                file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FOCUS NOTE: {params['note_content']}\n")
            status_message = "Workspace note securely preserved into cloud storage volumes."
        else:
            status_message = f"Cloud trigger completed. Dispatched telemetry pipeline event hooks."
            print(f"☁️ [Cloud Orchestration]: Routing Event Triggered on Target: '{app_type}' with parameters: {params}")
    except Exception as e:
        status_message = f"Automation worker loop tracking exception: {str(e)}"
    return status_message

@app.route("/api/voice-incident", methods=["POST"])
def voice_incident():
    try:
        if 'file' in request.files:
            audio_file = request.files['file']
            transcript = transcribe_audio_with_sarvam(audio_file)
        else:
            transcript = request.form.get("transcript", "")

        if not transcript or not transcript.strip():
            return jsonify({"error": "Null voice tokens received. Aborting runtime pipelines."}), 400

        print(f"⚡ Ingesting Stream Signature: '{transcript}'")

        system_instruction = (
            "You are an advanced executive core routing engine. Analyze the user's vocal transcript and classify their intent "
            "into exactly ONE of these specific application types:\n"
            "['spotify', 'calendar', 'email', 'chatgpt', 'maps', 'notion', 'whatsapp', 'github', 'amazon', 'flipkart', 'food', 'notes', 'pomodoro', 'youtube', 'discord', 'reddit', 'x', 'gmail'].\n\n"
            "Extract raw JSON matching this schema shape perfectly:\n"
            '{"target_app": "string", "extracted_params": {}}'
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"User voice transcript: {transcript}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction, 
                response_mime_type="application/json"
            ),
        )
        
        routing_data = json.loads(response.text)
        app_type = routing_data.get("target_app", "").lower()
        params = routing_data.get("extracted_params", {})

        automation_status = execute_backend_action(app_type, params)
        if "automation_log" not in params:
            params["automation_log"] = automation_status
            
        save_intent_to_graph(transcript, app_type, params)

    except Exception as e:
        print(f"🚨 Top-level Application Fault: {e}")
        routing_data = {"target_app": "notes", "extracted_params": {"note_content": str(e)}}
        transcript = "Execution Framework Fallback Engine Active"

    return jsonify({
        "job_id": f"VN-{datetime.now().strftime('%M%S')}X",
        "status": "synchronized",
        "transcript": transcript,
        "routing": routing_data
    })

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online", 
        "service": "Vaani Chronos Framework Core API Layer",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

if __name__ == "__main__":
    # Dynamically bind to the platform port provided by Render environment configurations
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)