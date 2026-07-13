# 🪐 VAANI | Neural Voice Intelligence Interface

VAANI is an immersive, next-generation full-stack voice intelligence matrix that translates real-time human speech intent into automated deep-link application routing. 

Built with a striking cyberpunk HUD aesthetic, the system bypasses traditional UI friction. It continuously captures vocal data packets from the browser, streams them to a cloud microservice container, isolates structural semantic parameters using AI intent extraction, and instantly flashes a dynamic routing card before dispatching the user to their target digital sector.

---

## 🚀 Live Core Systems & Deployment
* **Production HUD Interface:** `[Insert your live Vercel/Netlify/GitHub Pages URL here]`
* **Neural Pipeline Infrastructure (Backend Engine):** `https://vaani-m25h.onrender.com`

---

## ⚡ Hackathon Highlights & Core Capabilities

* **Autonomous Multitask Intent Parser:** Seamlessly classifies speech variables into specific software targets. It maps variables natively to **Pinterest** (Visual Matrix), **YouTube** (Stream Core), **Spotify** (Acoustic Ecosystem), **WhatsApp**, **ChatGPT**, and e-commerce nodes.
* **Fail-Safe Web Search Fallback:** Architecture engineered for zero runtime crashes. If the backend returns an unrecognized application command or raw transcription parameters, the application gracefully routes the intent to a Global Web Search dashboard.
* **Robust Param Extraction Shielding:** Implements client-side optional parameter chaining (`params?.query` / `params?.craving`). If the AI microservice encounters token omissions or structural shifts, the UI maps a default vector string instead of freezing the script thread.
* **Biometric Signal Interceptor:** Utilizes the hardware-level `MediaRecorder` API to convert live user voice captures into raw secure binary `.webm` blobs for dynamic network transmission.
* **Immersive Cyberpunk Matrix HUD:** Features a high-fidelity retro-futuristic styling suite including active scanline animation frames, CRT noise filter overlays, dynamic state-pulse color switches based on system loads, and mouse-reactive parallax grid shifts.

---

## 🛠️ The Architecture & Full-Stack Blueprint

### Frontend Architecture
* **Layout & Engine:** HTML5, Modern ES6+ JavaScript, Tailwind CSS (Form/Container Query engines).
* **Iconography & Systems:** Material Symbols Core, Sora, and JetBrains Mono cyber-grid typography.

### Backend Infrastructure
* **Microserver Core:** Python + Flask Web Framework.
* **Intelligence Processing:** Advanced Voice-to-Text Conversion & Deep Intent Parameter Extraction Frameworks (Leveraging Sarvam AI Processing Subsystems).

---

## 📊 Automated Dispatch Protocol Targets

When a user speaks into the biometric sensor node, the frontend system dynamically transforms extracted parameters into targeted operational pathways:

| Command Target | Vector Grid Address | Operational Parameter Managed |
| :--- | :--- | :--- |
| **Pinterest** | `https://in.pinterest.com/search/pins/?q=` | Visual moodboard & style generation (`params.query`) |
| **YouTube** | `https://www.youtube.com/results?search_query=` | Audio-visual grid rendering (`params.query`) |
| **Amazon / Flipkart**| Dedicated commercial query endpoints | E-commerce supply tracking (`params.product_query`) |
| **ChatGPT Console** | `https://chatgpt.com/?q=` | Cognitive raw vector injection (`params.ai_prompt`) |
| **Spotify Core** | `https://open.spotify.com/search/.../tracks` | Acoustic audio matrix focus tracking (`params.query`) |
| **Geo-Spatial Maps** | `https://www.google.com/maps/search/` | Location routing calculations (`params.location`) |

---

## 💻 Technical Execution & Run Procedures

### 1. Local Development Run
To launch the frontend dashboard framework locally, satisfy browser security layers by serving it over a clean network environment:
```bash
# Using Python microservers
python -m http.server 3000