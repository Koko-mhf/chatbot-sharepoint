"""
Connecteur SharePoint / Microsoft Graph API.
Permet de chercher des fichiers, lire des listes, etc.
Optionnel : fonctionne si les credentials Azure sont configurées.
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)


class SharePointConnector:
    """
    Connecteur vers Microsoft Graph API pour accéder à SharePoint,
    OneDrive et Teams programmatiquement.

    Utilise l'authentification App-Only (client_credentials).
    Optionnel — le chatbot fonctionne sans, mais avec moins de fonctionnalités.
    """

    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID", "")
        self.client_id = os.getenv("AZURE_CLIENT_ID", "")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET", "")
        self.site_url = os.getenv("SHAREPOINT_SITE_URL", "")
        self._token = None
        self.enabled = all([self.tenant_id, self.client_id, self.client_secret])

        if self.enabled:
            logger.info("✅ SharePoint Connector activé (Graph API)")
        else:
            logger.info(
                "ℹ️ SharePoint Connector désactivé "
                "(variables Azure non configurées — le bot fonctionne quand même)"
            )

    # ─── Authentification ─────────────────────────────────────

    def _get_token(self) -> str | None:
        """Obtient un token d'accès via client_credentials."""
        if not self.enabled:
            return None

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }

        try:
            resp = requests.post(url, data=data, timeout=10)
            resp.raise_for_status()
            self._token = resp.json().get("access_token")
            return self._token
        except Exception as e:
            logger.error(f"Erreur auth Graph API: {e}")
            return None

    def _headers(self) -> dict:
        """Headers HTTP avec le token."""
        token = self._token or self._get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    # ─── Recherche de fichiers ────────────────────────────────

    def search_files(self, query: str, top: int = 5) -> list[dict]:
        """
        Recherche des fichiers sur SharePoint via Graph API.

        Args:
            query: Termes de recherche.
            top: Nombre max de résultats.

        Returns:
            Liste de fichiers trouvés.
        """
        if not self.enabled:
            return []

        url = "https://graph.microsoft.com/v1.0/search/query"
        body = {
            "requests": [
                {
                    "entityTypes": ["driveItem"],
                    "query": {"queryString": query},
                    "from": 0,
                    "size": top,
                }
            ]
        }

        try:
            resp = requests.post(url, json=body, headers=self._headers(), timeout=15)
            resp.raise_for_status()
            hits = (
                resp.json()
                .get("value", [{}])[0]
                .get("hitsContainers", [{}])[0]
                .get("hits", [])
            )
            return [
                {
                    "name": hit.get("resource", {}).get("name", ""),
                    "url": hit.get("resource", {}).get("webUrl", ""),
                    "lastModified": hit.get("resource", {}).get(
                        "lastModifiedDateTime", ""
                    ),
                }
                for hit in hits
            ]
        except Exception as e:
            logger.error(f"Erreur recherche Graph API: {e}")
            return []

    # ─── Lire une liste SharePoint ────────────────────────────

    def get_list_items(self, site_id: str, list_id: str) -> list[dict]:
        """Récupère les éléments d'une liste SharePoint."""
        if not self.enabled:
            return []

        url = (
            f"https://graph.microsoft.com/v1.0/sites/{site_id}"
            f"/lists/{list_id}/items?expand=fields"
        )

        try:
            resp = requests.get(url, headers=self._headers(), timeout=15)
            resp.raise_for_status()
            return resp.json().get("value", [])
        except Exception as e:
            logger.error(f"Erreur lecture liste: {e}")
            return []

    def get_status(self) -> dict:
        """Statut du connecteur."""
        return {
            "enabled": self.enabled,
            "site_url": self.site_url or "non configuré",
        }
