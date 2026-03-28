"""
Chatbot SharePoint - Backend Flask
Utilise Groq + LLaMA 3 pour répondre aux questions
sur SharePoint, Teams, OneDrive et Microsoft 365.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

from llm_client import LLMClient
from knowledge_base import KnowledgeBase
from memory_store import MemoryStore
from sharepoint_connector import SharePointConnector

# ─── Config ───────────────────────────────────────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="../FRONTEND", static_url_path="")
CORS(app)  # Nécessaire pour l'iframe SharePoint

# ─── Initialisation des services ──────────────────────────────
knowledge_base = KnowledgeBase()
memory_store = MemoryStore()
llm_client = LLMClient()
sharepoint_connector = SharePointConnector()


# ─── Routes API ───────────────────────────────────────────────

@app.route("/")
def index():
    """Sert le frontend (chat.html)."""
    return send_from_directory("../FRONTEND", "chat.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint principal du chatbot.
    Body JSON : { "message": "...", "session_id": "..." }
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_message:
        return jsonify({"error": "Message vide"}), 400

    try:
        # 1. Récupérer l'historique de conversation
        history = memory_store.get_history(session_id)

        # 2. Chercher le contexte pertinent dans la base de connaissances
        context_docs = knowledge_base.search(user_message)

        # 3. Envoyer au LLM (Groq + LLaMA 3)
        response_text = llm_client.generate_response(
            user_message=user_message,
            context_docs=context_docs,
            conversation_history=history,
        )

        # 4. Sauvegarder dans l'historique
        memory_store.add_message(session_id, "user", user_message)
        memory_store.add_message(session_id, "assistant", response_text)

        return jsonify({
            "response": response_text,
            "session_id": session_id,
            "sources": [doc.get("title", "") for doc in context_docs],
        })

    except Exception as e:
        logger.error(f"Erreur chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_history():
    """Efface l'historique d'une session."""
    data = request.get_json()
    session_id = data.get("session_id", "default")
    memory_store.clear(session_id)
    return jsonify({"status": "ok"})


@app.route("/api/health", methods=["GET"])
def health():
    """Health check pour vérifier que le serveur tourne."""
    return jsonify({
        "status": "ok",
        "llm": llm_client.get_status(),
        "knowledge_docs": knowledge_base.count(),
    })


# ─── Lancement ────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    logger.info(f" Chatbot SharePoint démarré sur http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
