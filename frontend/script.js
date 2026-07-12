// 🌐 frontend/script.js

let mediaRecorder;
let audioChunks = [];

document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("start-btn"); 
    const stopBtn = document.getElementById("stop-btn");   
    const statusText = document.getElementById("status-text");

    if (startBtn && stopBtn) {
        startBtn.addEventListener("click", startRecording);
        stopBtn.addEventListener("click", stopRecording);
    } else {
        console.warn("⚠️ UI Buttons not found in index.html configuration.");
    }
});

async function startRecording() {
    audioChunks = []; 
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.webm');

            updateUIStatus("Processing audio through VAANI pipeline...");

            try {
                const response = await fetch('https://vaani-m25h.onrender.com/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error("Flask execution fault.");

                const data = await response.json();
                console.log("🚀 Server packet returned:", data);
                updateDashboardUI(data);

            } catch (err) {
                console.error("❌ Pipeline API transmission failed:", err);
                updateUIStatus("Network Connection Failure. Is Flask running?");
            }
        };

        mediaRecorder.start();
        updateUIStatus("🔴 Recording Voice Stream Live...");
    } catch (err) {
        console.error("Microphone access denied:", err);
        updateUIStatus("Microphone access blocked.");
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        updateUIStatus("Processing transmission stream...");
    }
}

function updateUIStatus(text) {
    const statusElement = document.getElementById("status-text");
    if (statusElement) statusElement.innerText = text;
}

function updateDashboardUI(data) {
    updateUIStatus("✅ Event Analyzed Successfully!");

    const transcriptBox = document.getElementById("transcript-box");
    const incidentBadge = document.getElementById("incident-badge");
    const resourceText = document.getElementById("resource-text");
    const sectorText = document.getElementById("sector-text");
    const dbStatusBanner = document.getElementById("db-status-banner"); 

    if (transcriptBox) transcriptBox.innerText = `"${data.transcript}"`;
    if (incidentBadge) incidentBadge.innerText = data.incident_type;
    if (resourceText) resourceText.innerText = data.allocated_resource;
    if (sectorText) sectorText.innerText = data.sector;

    // 🚨 REPORT THE ROUTING STATUS LIVE ON THE DASHBOARD DISPLAY
    if (dbStatusBanner) {
        if (data.workflow_engine_status.db_status === "FALLBACK_LOCAL") {
            dbStatusBanner.innerText = "⚠️ SYSTEM WARNING: Neo4j Cloud Port 7687 Blocked. Local Core Ledger Engaged.";
            dbStatusBanner.style.backgroundColor = "#e74c3c"; 
            dbStatusBanner.style.color = "white";
        } else {
            dbStatusBanner.innerText = "⚡ Neo4j Aura Cloud Node: Synchronized and Active.";
            dbStatusBanner.style.backgroundColor = "#2ecc71"; 
            dbStatusBanner.style.color = "white";
        }
    }
}