#  Chatbot SharePoint — Assistant Microsoft 365

Chatbot d'aide aux outils **SharePoint, Teams, OneDrive** propulsé par **Groq + LLaMA 3** .

##  Ce qui a changé

| Avant (ancien) | Maintenant (nouveau) |
|---|---|
| TensorFlow / scikit-learn |  **Groq + LLaMA 3** (LLM gratuit) |
| Modèles .pkl à entraîner |  Zéro entraînement nécessaire |
| Intent classifier maison |  LLM comprend tout nativement |
| Réponses limitées/statiques | Réponses intelligentes et contextuelles |
|  Pas de mémoire |  Historique de conversation |
|  Pas de Microsoft Learn |  Liens Microsoft Learn intégrés |

##  Structure du projet

```
CHATBOT-SHAREPOINT/
├── API/
│   ├── app.py                  ← Backend Flask (point d'entrée)
│   ├── llm_client.py           ← Client Groq + LLaMA 3
│   ├── knowledge_base.py       ← Base de connaissances + Microsoft Learn
│   ├── memory_store.py         ← Historique des conversations
│   └── sharepoint_connector.py ← Connecteur Microsoft Graph (optionnel)
├── DATA/
│   └── knowledge_documents.json ← Documents d'aide SharePoint/Teams/OneDrive
├── FRONTEND/
│   ├── chat.html               ← Interface du chatbot (iframe SharePoint)
│   ├── chat.css                ← Styles (thème Microsoft)
│   └── chat.js                 ← Logique frontend
├── TESTS/
│   └── test_chatbot.py         ← Tests unitaires
├── .env.example                ← Template de configuration
├── requirements.txt            ← Dépendances Python
└── README.md
```
