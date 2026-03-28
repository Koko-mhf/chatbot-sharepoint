"""
Mémoire conversationnelle — stocke l'historique par session.
Stockage en mémoire (RAM). Se réinitialise au redémarrage du serveur.
"""

import logging
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)

MAX_HISTORY = 50  # Messages max par session


class MemoryStore:
    """Stockage en mémoire de l'historique des conversations."""

    def __init__(self):
        self._sessions: dict[str, list[dict]] = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str):
        """
        Ajoute un message à l'historique d'une session.

        Args:
            session_id: Identifiant de la session.
            role: 'user' ou 'assistant'.
            content: Contenu du message.
        """
        self._sessions[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })

        # Limiter la taille de l'historique
        if len(self._sessions[session_id]) > MAX_HISTORY:
            self._sessions[session_id] = self._sessions[session_id][-MAX_HISTORY:]

    def get_history(self, session_id: str) -> list[dict]:
        """Retourne l'historique d'une session."""
        return self._sessions.get(session_id, [])

    def clear(self, session_id: str):
        """Efface l'historique d'une session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"🗑️ Session {session_id} effacée")

    def get_active_sessions(self) -> int:
        """Nombre de sessions actives."""
        return len(self._sessions)
