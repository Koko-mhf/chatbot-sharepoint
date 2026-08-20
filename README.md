# Assistant M365 (Zo) - Chatbot IA pour SharePoint

**Projet de fin d'études / Stage de 3ème année (Cycle Ingénieur CESI) réalisé au sein d'ONZORA**.

## Description du Projet

Ce projet consiste en la conception, l'entraînement et le déploiement d'un agent conversationnel (chatbot) nommé Zo, intégré nativement à un portail de communication SharePoint. 

Développé pour faciliter l'adoption de l'écosystème Microsoft 365 (SharePoint, Teams, OneDrive), cet assistant répond en langage naturel aux questions des collaborateurs[cite: 1]. Il s'appuie sur une approche strictement pragmatique de l'Intelligence Artificielle, axée sur l'utilité, la sécurité des données et l'efficacité des modèles via une architecture RAG (Retrieval-Augmented Generation)[cite: 1].

---

## ️ Architecture Technique

L'architecture se décompose en quatre couches principales, garantissant performance et sécurité[cite: 1] :

### 1. Couche IA et Modèle de Langage (LLM)
* **Modèle utilisé :** LLaMA 3.3 70B de Meta, accédé via l'API gratuite Groq pour une inférence ultra-rapide (LPU)[cite: 1].
* **Pipeline RAG :** Les requêtes utilisateur sont enrichies grâce à une recherche contextuelle dans une base de connaissances locale au format JSON (`knowledge_documents.json`) contenant les documentations M365[cite: 1].
* **Traitement du Langage Naturel (NLP) :** Implémentation de la tokenization et de la lemmatization pour filtrer le bruit, normaliser les mots et améliorer significativement la robustesse du modèle face aux variations morphologiques[cite: 1].

### 2. Couche Backend (API REST)
* **Technologie :** API REST développée en Python avec le framework Flask[cite: 1].
* **Hébergement :** Déploiement sécurisé en HTTPS via Render.com avec Gunicorn[cite: 1].
* **Gestion de la mémoire :** Implémentation d'un système de mémoire conversationnelle par session[cite: 1]. L'historique conserve les 50 derniers messages en RAM, et les 10 derniers échanges sont injectés dans le prompt LLM pour maintenir le contexte[cite: 1].

### 3. Couche Frontend (SharePoint Framework - SPFx)
* **Interface :** Bulle de chat flottante au design adaptatif (thème sombre/clair) avec icône animée, typographie DM Sans et JetBrains Mono, et accent violet[cite: 1].
* **Technologie :** Composant développé en React et TypeScript, déployé sous forme d'extension SPFx (Application Customizer) pour s'injecter sur toutes les pages du portail SharePoint[cite: 1].

---

## Défis Techniques Relevés

Durant le développement, plusieurs verrous technologiques ont été levés :

* **Gestion stricte des CORS :** Résolution des blocages liés à la politique same-origin de SharePoint Online en configurant précisément les en-têtes CORS (Access-Control-Allow-Origin, Headers, Methods) sur le serveur Flask[cite: 1].
* **Stabilité de l'environnement :** Migration du générateur PnP SPFx vers le générateur Microsoft officiel (`@microsoft/generator-sharepoint v1.17.4`) pour résoudre des conflits de dépendances binaires (node-sass et Python)[cite: 1].
* **Prompt Engineering :** Construction de prompts système avancés définissant un rôle strict d'expert Microsoft 365, imposant un formatage précis (étapes numérotées) et limitant les hallucinations[cite: 1].

---

##  Stack Technologique

**Data Science & Backend**
* Python 3 | Flask | Flask-CORS[cite: 1]
* LLM : LLaMA 3.3 70B | Groq SDK[cite: 1]
* Algorithmique : Vectorisation Bag-of-words, Lemmatization, Softmax[cite: 1]

**Frontend & Intégration Microsoft**
* React (v17.0.1) | TypeScript (v4.7.4) | SCSS Modules[cite: 1]
* SharePoint Framework (SPFx v1.15+) | Node.js (v16.20.2 LTS) | Gulp[cite: 1]
* Microsoft 365 (SharePoint Online, Teams, OneDrive)[cite: 1]

---

## ️ Installation et Déploiement

### Prérequis
* Node.js v16.x et Gulp CLI[cite: 1].
* Un tenant Microsoft 365 avec accès au catalogue d'applications (App Catalog)[cite: 1].
* Une clé API Groq valide[cite: 1].

### Lancement Backend (Flask)
```bash
pip install -r requirements.txt
# Configurer le fichier .env avec la clé GROQ_API_KEY
python app.py
