# 🤖 Chatbot SharePoint — Assistant Microsoft 365

Chatbot d'aide aux outils **SharePoint, Teams, OneDrive** propulsé par **Groq + LLaMA 3** (gratuit).

## ✅ Ce qui a changé

| Avant (ancien) | Maintenant (nouveau) |
|---|---|
| ❌ TensorFlow / scikit-learn | ✅ **Groq + LLaMA 3** (LLM gratuit) |
| ❌ Modèles .pkl à entraîner | ✅ Zéro entraînement nécessaire |
| ❌ Intent classifier maison | ✅ LLM comprend tout nativement |
| ❌ Réponses limitées/statiques | ✅ Réponses intelligentes et contextuelles |
| ❌ Pas de mémoire | ✅ Historique de conversation |
| ❌ Pas de Microsoft Learn | ✅ Liens Microsoft Learn intégrés |

## 📁 Structure du projet

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

## 🚀 Installation

### 1. Clé API Groq (gratuite)

1. Va sur **https://console.groq.com**
2. Crée un compte (gratuit)
3. Va dans **API Keys** → **Create API Key**
4. Copie la clé

### 2. Configuration

```bash
# Copier le fichier de config
cp .env.example .env

# Coller ta clé Groq dans .env
# GROQ_API_KEY=gsk_ta_clé_ici
```

### 3. Installation des dépendances

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer (Windows)
.venv\Scripts\activate

# Activer (Mac/Linux)
source .venv/bin/activate

# Installer les packages
pip install -r requirements.txt
```

### 4. Lancer le chatbot

```bash
cd API
python app.py
```

→ Ouvre **http://localhost:5000** dans ton navigateur 🎉

### 5. Tests

```bash
pytest TESTS/test_chatbot.py -v
```

## 🖥️ Intégrer dans SharePoint (iframe)

1. Sur ta page SharePoint, clique sur **Modifier**
2. Ajoute le composant WebPart **Incorporer** (Embed)
3. Colle l'URL de ton serveur :
   ```
   <iframe src="https://ton-serveur.com" width="100%" height="600" frameborder="0"></iframe>
   ```
4. Pour un hébergement gratuit : déploie sur **Render.com** ou **Railway.app**

## 📦 Ce qu'il faut installer (résumé)

| Package | Rôle | Gratuit ? |
|---|---|---|
| `flask` | Backend API | ✅ |
| `flask-cors` | CORS pour iframe | ✅ |
| `groq` | Client API Groq (LLaMA 3) | ✅ |
| `python-dotenv` | Variables d'environnement | ✅ |
| `requests` | Appels HTTP (Graph API) | ✅ |
| `pytest` | Tests | ✅ |

**Total : 0 €**

## ❌ Fichiers à supprimer (ancien code)

Tu peux supprimer ces fichiers de ton ancien projet :
- `MODELS/intent_classifier.pkl`
- `MODELS/vectorizer.pkl`
- `MODELS/train_model.py`
- `DATA/training_data.json`
- `DATA/responses.json`
- `DATA/intents.json`
- `DATA/generate_variation.py`
- `API/chatbot.py` (remplacé par `llm_client.py`)
- `API/engine.py` (remplacé par la logique dans `app.py`)
