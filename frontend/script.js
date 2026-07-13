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
        
        // 🍏 SAFARI / CROSS-BROWSER FALLBACK
        // WebM is native on Chrome/Firefox. Safari (Mac/iOS) requires an MP4 fallback container.
        let options = { mimeType: 'audio/webm' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            options = { mimeType: 'audio/mp4' };
        }

        mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: options.mimeType });
            const formData = new FormData();
            
            // Derive extension match from assigned audio profile container type
            const fileExtension = options.mimeType.includes('mp4') ? 'mp4' : 'webm';
            formData.append('file', audioBlob, `recording.${fileExtension}`);

            updateUIStatus("Processing audio through VAANI pipeline...");

            try {
                const response = await fetch('https://vaani-m25h.onrender.com/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error(`Flask execution fault. Status Code: ${response.status}`);

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
        mediaRecorder.stream.getTracks().forEach(track => track.stop()); // Clean hardware states
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

    // Robust default text fallbacks preventing ugly "undefined" strings
    if (transcriptBox) transcriptBox.innerText = data?.transcript ? `"${data.transcript}"` : `"No text parsed"`;
    if (incidentBadge) incidentBadge.innerText = data?.incident_type || "UNKNOWN";
    if (resourceText) resourceText.innerText = data?.allocated_resource || "UNASSIGNED";
    if (sectorText) sectorText.innerText = data?.sector || "NONE";

    // 🚨 OPTIONAL CHAINING GUARD
    // If workflow_engine_status isn't present, using optional chaining prevents a total script crash
    if (dbStatusBanner) {
        const dbStatus = data?.workflow_engine_status?.db_status;
        
        if (dbStatus === "FALLBACK_LOCAL") {
            dbStatusBanner.innerText = "⚠️ SYSTEM WARNING: Neo4j Cloud Port 7687 Blocked. Local Core Ledger Engaged.";
            dbStatusBanner.style.backgroundColor = "#e74c3c"; 
            dbStatusBanner.style.color = "white";
        } else if (dbStatus === "CONNECTED" || dbStatus === "ACTIVE" || data?.workflow_engine_status) {
            dbStatusBanner.innerText = "⚡ Neo4j Aura Cloud Node: Synchronized and Active.";
            dbStatusBanner.style.backgroundColor = "#2ecc71"; 
            dbStatusBanner.style.color = "white";
        } else {
            dbStatusBanner.innerText = "🛑 Ledger Status Unknown. Microservice Unreachable.";
            dbStatusBanner.style.backgroundColor = "#7f8c8d";
            dbStatusBanner.style.color = "white";
        }
    }
}