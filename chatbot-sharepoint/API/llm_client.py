"""
Client LLM — Groq + LLaMA 3 (gratuit).
Gère le prompt système, le contexte SharePoint et l'appel API.
"""

import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

# ─── Prompt système ───────────────────────────────────────────

SYSTEM_PROMPT = """Tu es Zo, un assistant expert Microsoft 365. Tu aides les utilisateurs
avec SharePoint, Microsoft Teams, OneDrive, et les outils Microsoft 365.

Règles :
1. Tu t'appelles Zo. Ne te présente jamais autrement.
2. Réponds TOUJOURS en français, sauf si l'utilisateur écrit en anglais.
3. Sois concis et pratique : donne des étapes claires et numérotées.
4. Si tu ne connais pas la réponse, dis-le honnêtement.
5. Utilise le CONTEXTE fourni ci-dessous pour répondre précisément.
6. Si la question ne concerne pas Microsoft 365, redirige poliment l'utilisateur.
7. Propose des liens Microsoft Learn quand c'est pertinent.
8. N'utilise JAMAIS d'emojis dans tes réponses. Jamais.

Tu dois être professionnel, direct, et aller droit au but."""


class LLMClient:
    """Client pour l'API Groq avec LLaMA 3."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ GROQ_API_KEY manquante ! "
                "Crée un compte gratuit sur https://console.groq.com "
                "et ajoute ta clé dans le fichier .env"
            )
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
        logger.info(f"✅ LLM initialisé : {self.model}")

    def generate_response(
        self,
        user_message: str,
        context_docs: list[dict],
        conversation_history: list[dict],
    ) -> str:
        """
        Génère une réponse via Groq + LLaMA 3.

        Args:
            user_message: La question de l'utilisateur.
            context_docs: Documents pertinents de la base de connaissances.
            conversation_history: Historique de la conversation.

        Returns:
            La réponse générée par le LLM.
        """
        # Construire le contexte à partir des documents trouvés
        context_text = self._build_context(context_docs)

        # Construire les messages pour l'API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Ajouter le contexte si on en a
        if context_text:
            messages.append({
                "role": "system",
                "content": f"CONTEXTE (base de connaissances) :\n{context_text}",
            })

        # Ajouter l'historique (les 10 derniers échanges max)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
            })

        # Ajouter la question de l'utilisateur
        messages.append({"role": "user", "content": user_message})

        # Appel API Groq
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Erreur API Groq: {e}")
            return (
                "Désolé, je rencontre un problème technique. "
                "Réessaie dans quelques secondes."
            )

    def _build_context(self, docs: list[dict]) -> str:
        """Formate les documents de contexte pour le prompt."""
        if not docs:
            return ""

        parts = []
        for i, doc in enumerate(docs, 1):
            title = doc.get("title", "Sans titre")
            content = doc.get("content", "")
            source = doc.get("source", "")
            parts.append(f"[{i}] {title}\n{content}\n(Source : {source})")

        return "\n\n".join(parts)

    def get_status(self) -> dict:
        """Retourne le statut du client LLM."""
        return {
            "provider": "Groq",
            "model": self.model,
            "status": "ok",
        }
