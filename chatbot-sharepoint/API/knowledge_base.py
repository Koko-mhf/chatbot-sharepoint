"""
Base de connaissances — SharePoint, Teams, OneDrive.
Recherche locale (JSON) + scraping Microsoft Learn.
"""

import json
import os
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "DATA"


class KnowledgeBase:
    """
    Base de connaissances hybride :
    - Documents locaux (knowledge_documents.json)
    - Liens Microsoft Learn générés dynamiquement
    """

    def __init__(self):
        self.documents = self._load_documents()
        logger.info(f" Base de connaissances : {len(self.documents)} documents chargés")

    # ─── Chargement ───────────────────────────────────────────

    def _load_documents(self) -> list[dict]:
        """Charge les documents depuis le fichier JSON."""
        filepath = DATA_DIR / "knowledge_documents.json"
        if not filepath.exists():
            logger.warning(f" Fichier introuvable : {filepath}")
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else data.get("documents", [])
        except Exception as e:
            logger.error(f"Erreur chargement documents: {e}")
            return []

    # ─── Recherche ────────────────────────────────────────────

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Recherche les documents les plus pertinents pour la requête.
        Utilise une recherche par mots-clés (simple et efficace).

        Args:
            query: La question de l'utilisateur.
            top_k: Nombre max de résultats.

        Returns:
            Liste de documents pertinents.
        """
        query_lower = query.lower()
        query_words = set(re.findall(r"\w+", query_lower))

        scored_docs = []
        for doc in self.documents:
            score = self._compute_score(query_words, query_lower, doc)
            if score > 0:
                scored_docs.append((score, doc))

        # Trier par score décroissant
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        results = [doc for _, doc in scored_docs[:top_k]]

        # Ajouter des liens Microsoft Learn pertinents
        learn_links = self._get_learn_links(query_lower)
        if learn_links:
            results.append({
                "title": "📖 Ressources Microsoft Learn",
                "content": "\n".join(learn_links),
                "source": "Microsoft Learn",
            })

        return results

    def _compute_score(
        self, query_words: set, query_lower: str, doc: dict
    ) -> float:
        """Calcule un score de pertinence pour un document."""
        score = 0.0

        # Mots-clés dans le titre (poids fort)
        title = doc.get("title", "").lower()
        title_words = set(re.findall(r"\w+", title))
        title_matches = query_words & title_words
        score += len(title_matches) * 3.0

        # Mots-clés dans les tags
        tags = [t.lower() for t in doc.get("tags", [])]
        for tag in tags:
            if tag in query_lower:
                score += 2.0

        # Mots-clés dans le contenu (poids faible)
        content = doc.get("content", "").lower()
        content_words = set(re.findall(r"\w+", content))
        content_matches = query_words & content_words
        score += len(content_matches) * 0.5

        # Catégorie qui match
        category = doc.get("category", "").lower()
        if category and category in query_lower:
            score += 2.0

        return score

    # ─── Microsoft Learn ──────────────────────────────────────

    def _get_learn_links(self, query: str) -> list[str]:
        """Génère des liens Microsoft Learn pertinents."""
        links = []

        learn_map = {
            "sharepoint": {
                "keywords": ["sharepoint", "site", "bibliothèque", "liste", "page", "webpart"],
                "links": [
                    "📌 Guide SharePoint : https://learn.microsoft.com/fr-fr/sharepoint/",
                    "📌 Créer un site : https://learn.microsoft.com/fr-fr/sharepoint/create-site-collection",
                ],
            },
            "teams": {
                "keywords": ["teams", "réunion", "canal", "équipe", "appel", "visio"],
                "links": [
                    "📌 Guide Teams : https://learn.microsoft.com/fr-fr/microsoftteams/",
                    "📌 Gestion d'équipes : https://learn.microsoft.com/fr-fr/microsoftteams/get-started-with-teams-create-your-first-teams-and-channels",
                ],
            },
            "onedrive": {
                "keywords": ["onedrive", "fichier", "synchron", "partage", "stockage"],
                "links": [
                    "📌 Guide OneDrive : https://learn.microsoft.com/fr-fr/onedrive/",
                    "📌 Sync : https://learn.microsoft.com/fr-fr/onedrive/one-drive-sync",
                ],
            },
            "power_automate": {
                "keywords": ["power automate", "flux", "automatisation", "workflow"],
                "links": [
                    "📌 Power Automate : https://learn.microsoft.com/fr-fr/power-automate/",
                ],
            },
            "permissions": {
                "keywords": ["permission", "accès", "droit", "partage", "sécurité", "autorisation"],
                "links": [
                    "📌 Permissions SharePoint : https://learn.microsoft.com/fr-fr/sharepoint/understanding-permission-levels",
                ],
            },
        }

        for _category, data in learn_map.items():
            if any(kw in query for kw in data["keywords"]):
                links.extend(data["links"])

        return links[:4]  # Max 4 liens

    # ─── Utilitaires ──────────────────────────────────────────

    def count(self) -> int:
        """Nombre de documents dans la base."""
        return len(self.documents)

    def reload(self):
        """Recharge les documents depuis le fichier."""
        self.documents = self._load_documents()
        logger.info(f"🔄 Base rechargée : {len(self.documents)} documents")
