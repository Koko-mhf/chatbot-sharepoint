"""
Tests du chatbot SharePoint.
Lance avec : pytest TESTS/test_chatbot.py -v
"""

import json
import sys
from pathlib import Path

# Ajouter le dossier API au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "API"))


# ─── Tests Knowledge Base ─────────────────────────────────────

def test_knowledge_base_loads():
    """La base de connaissances doit se charger sans erreur."""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    assert kb.count() > 0, "Aucun document chargé"


def test_knowledge_base_search_sharepoint():
    """Recherche SharePoint doit retourner des résultats."""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    results = kb.search("créer un site SharePoint")
    assert len(results) > 0, "Aucun résultat pour 'créer un site SharePoint'"


def test_knowledge_base_search_teams():
    """Recherche Teams doit retourner des résultats."""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    results = kb.search("réunion Teams")
    assert len(results) > 0, "Aucun résultat pour 'réunion Teams'"


def test_knowledge_base_search_onedrive():
    """Recherche OneDrive doit retourner des résultats."""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    results = kb.search("synchroniser OneDrive")
    assert len(results) > 0, "Aucun résultat pour 'synchroniser OneDrive'"


def test_knowledge_base_learn_links():
    """Les liens Microsoft Learn doivent être générés."""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    results = kb.search("permissions SharePoint")
    has_learn = any("Microsoft Learn" in doc.get("source", "") for doc in results)
    assert has_learn, "Pas de liens Microsoft Learn trouvés"


# ─── Tests Memory Store ───────────────────────────────────────

def test_memory_store():
    """L'historique de conversation doit fonctionner."""
    from memory_store import MemoryStore
    ms = MemoryStore()

    ms.add_message("test_session", "user", "Bonjour")
    ms.add_message("test_session", "assistant", "Bonjour ! Comment puis-je aider ?")

    history = ms.get_history("test_session")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_memory_store_clear():
    """L'effacement de session doit fonctionner."""
    from memory_store import MemoryStore
    ms = MemoryStore()

    ms.add_message("to_clear", "user", "Test")
    ms.clear("to_clear")

    history = ms.get_history("to_clear")
    assert len(history) == 0


# ─── Tests données JSON ──────────────────────────────────────

def test_knowledge_documents_valid_json():
    """Le fichier knowledge_documents.json doit être valide."""
    filepath = Path(__file__).resolve().parent.parent / "DATA" / "knowledge_documents.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list), "Le JSON doit être une liste"
    assert len(data) > 0, "Le JSON ne doit pas être vide"

    for doc in data:
        assert "id" in doc, f"Document sans id : {doc}"
        assert "title" in doc, f"Document sans title : {doc}"
        assert "content" in doc, f"Document sans content : {doc}"


# ─── Tests Flask App ─────────────────────────────────────────

def test_flask_health(monkeypatch):
    """Le endpoint /api/health doit répondre."""
    monkeypatch.setenv("GROQ_API_KEY", "fake_key_for_testing")

    from app import app
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
