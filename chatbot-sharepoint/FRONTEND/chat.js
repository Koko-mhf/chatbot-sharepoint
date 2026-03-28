/**
 * Zo — Assistant Microsoft 365
 * Frontend JavaScript
 */

// ─── Config ──────────────────────────────────────────────────

const API_URL = window.location.origin + "/api";
const SESSION_ID =
    sessionStorage.getItem("zo_session") ||
    "zo_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8);
sessionStorage.setItem("zo_session", SESSION_ID);

// ─── SVG Icons (pas d'emojis) ────────────────────────────────

const SPARKLE_SVG = `<svg class="sparkle-icon-sm" viewBox="0 0 24 24" fill="none"><path d="M12 2L13.09 8.26L18 6L14.74 10.91L21 12L14.74 13.09L18 18L13.09 15.74L12 22L10.91 15.74L6 18L9.26 13.09L3 12L9.26 10.91L6 6L10.91 8.26L12 2Z" fill="currentColor"/></svg>`;

const USER_SVG = `<svg class="user-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;

// ─── DOM ─────────────────────────────────────────────────────

const messagesContainer = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const btnSend = document.getElementById("btn-send");
const btnClear = document.getElementById("btn-clear");
const quickSuggestions = document.getElementById("quick-suggestions");

let isLoading = false;

// ─── Envoi de message ────────────────────────────────────────

async function sendMessage(text) {
    const message = text || chatInput.value.trim();
    if (!message || isLoading) return;

    appendMessage("user", message);
    chatInput.value = "";
    chatInput.style.height = "auto";

    quickSuggestions.style.display = "none";

    isLoading = true;
    btnSend.disabled = true;
    const typingEl = showTypingIndicator();

    try {
        const response = await fetch(API_URL + "/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                session_id: SESSION_ID,
            }),
        });

        const data = await response.json();
        typingEl.remove();

        if (response.ok) {
            appendMessage("bot", data.response, data.sources);
        } else {
            appendMessage("bot", "Erreur : " + (data.error || "Une erreur est survenue."));
        }
    } catch (error) {
        typingEl.remove();
        appendMessage("bot", "Impossible de contacter le serveur. Vérifiez que le backend est démarré.");
        console.error("Erreur réseau:", error);
    } finally {
        isLoading = false;
        btnSend.disabled = false;
        chatInput.focus();
    }
}

// ─── Affichage des messages ──────────────────────────────────

function appendMessage(role, content, sources = []) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + (role === "user" ? "user-message" : "bot-message");

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML = role === "user" ? USER_SVG : SPARKLE_SVG;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = formatMessage(content);

    if (sources && sources.length > 0) {
        const filtered = sources.filter(Boolean);
        if (filtered.length > 0) {
            const sourcesDiv = document.createElement("div");
            sourcesDiv.className = "sources";
            sourcesDiv.textContent = "Sources : " + filtered.join(", ");
            bubble.appendChild(sourcesDiv);
        }
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(text) {
    if (!text) return "";

    let html = text
        .replace(/```(\w*)\n([\s\S]*?)```/g, "<pre><code>$2</code></pre>")
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.+?)\*/g, "<em>$1</em>")
        .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>')
        .replace(/^(\d+)\.\s+(.+)$/gm, "<li>$2</li>")
        .replace(/^[-•]\s+(.+)$/gm, "<li>$1</li>")
        .replace(/\n\n/g, "</p><p>")
        .replace(/\n/g, "<br>");

    html = "<p>" + html + "</p>";
    html = html.replace(/(<li>.*?<\/li>)+/g, "<ul>$&</ul>");

    return html;
}

// ─── Typing indicator ────────────────────────────────────────

function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message";
    typingDiv.innerHTML = `
        <div class="message-avatar">${SPARKLE_SVG}</div>
        <div class="message-bubble">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingDiv;
}

// ─── Clear ───────────────────────────────────────────────────

async function clearConversation() {
    try {
        await fetch(API_URL + "/clear", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID }),
        });
    } catch (e) {
        console.error("Erreur clear:", e);
    }

    const messages = messagesContainer.querySelectorAll(".message");
    messages.forEach((msg, index) => {
        if (index > 0) msg.remove();
    });

    quickSuggestions.style.display = "flex";
    chatInput.focus();
}

// ─── Auto-resize ─────────────────────────────────────────────

function autoResize() {
    chatInput.style.height = "auto";
    chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + "px";
}

// ─── Events ──────────────────────────────────────────────────

btnSend.addEventListener("click", () => sendMessage());
btnClear.addEventListener("click", clearConversation);

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

chatInput.addEventListener("input", autoResize);

document.querySelectorAll(".suggestion").forEach((btn) => {
    btn.addEventListener("click", () => {
        sendMessage(btn.dataset.question);
    });
});

chatInput.focus();
