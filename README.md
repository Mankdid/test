# 🚀 AI Website Generator

Un service de génération automatisée de sites web professionnels avec l'Intelligence Artificielle, inspiré de ZipWP.

## 📋 Description

AI Website Generator est un outil puissant qui permet de créer des sites web complets et professionnels en moins de 60 secondes. Propulsé par Claude AI d'Anthropic, il génère automatiquement:

- 🏗️ **Structure du site** (sitemap, navigation)
- ✍️ **Contenu professionnel** (textes SEO-optimisés)
- 🎨 **Design moderne** (layouts responsive)
- 🌈 **Schémas de couleurs** adaptés à votre secteur
- 📱 **Sites mobile-friendly**
- 🌍 **Support multi-langues**

## ✨ Fonctionnalités principales

### Génération ultra-rapide
- Site complet généré en ~60 secondes
- Interface intuitive et simple d'utilisation
- Aucune compétence technique requise

### IA puissante
- Propulsé par Claude AI (modèle Sonnet 4)
- Génération de contenu contextuel et pertinent
- Adaptation automatique au secteur d'activité

### Personnalisation
- Choix du secteur d'activité
- Sélection des pages à inclure
- Support de 5 langues (FR, EN, ES, DE, IT)
- Génération de schémas de couleurs harmonieux

### Export facile
- Prévisualisation en temps réel
- Téléchargement en ZIP
- Code HTML/CSS/JS propre et lisible

## 🛠️ Technologies utilisées

### Backend
- **FastAPI** - Framework web moderne et performant
- **Python 3.8+**
- **Anthropic Claude API** - Intelligence artificielle
- **Jinja2** - Moteur de templates
- **Pydantic** - Validation des données

### Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**
- **Design responsive**
- **Animations CSS**

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Clé API Anthropic (Claude AI)
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone <url-du-repo>
cd test
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
```

Éditer le fichier `.env` et ajouter votre clé API:
```env
ANTHROPIC_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
```

5. **Créer les dossiers nécessaires**
```bash
mkdir -p generated_sites templates
```

## 🚀 Démarrage

### Lancer le serveur

```bash
python backend/main.py
```

Le serveur démarre sur `http://localhost:8000`

### Utilisation

1. Ouvrir votre navigateur à `http://localhost:8000`
2. Remplir le formulaire:
   - Nom de votre entreprise
   - Description de votre activité
   - Secteur d'activité (optionnel)
   - Public cible (optionnel)
   - Langue souhaitée
   - Pages à inclure (optionnel)
3. Cliquer sur "Générer mon site web"
4. Attendre ~60 secondes
5. Prévisualiser et télécharger votre site!

## 📁 Structure du projet

```
test/
├── backend/
│   ├── __init__.py
│   ├── main.py              # API FastAPI principale
│   ├── ai_generator.py      # Génération de contenu IA
│   └── website_builder.py   # Construction HTML/CSS/JS
├── frontend/
│   ├── index.html           # Interface utilisateur
│   ├── style.css            # Styles
│   └── script.js            # Logique frontend
├── templates/               # Templates de base
├── generated_sites/         # Sites générés (créé automatiquement)
├── requirements.txt         # Dépendances Python
├── .env.example            # Variables d'environnement exemple
├── .gitignore
└── README.md
```

## 🔧 API Endpoints

### `POST /api/generate`
Génère un site web complet.

**Corps de la requête:**
```json
{
  "business_name": "Mon Entreprise",
  "business_description": "Description de l'activité...",
  "industry": "technology",
  "target_audience": "Professionnels",
  "language": "fr",
  "pages": ["Accueil", "Services", "Contact"]
}
```

**Réponse:**
```json
{
  "site_id": "mon-entreprise-abc123",
  "preview_url": "/api/preview/mon-entreprise-abc123",
  "download_url": "/api/download/mon-entreprise-abc123",
  "pages": ["index", "services", "contact"],
  "message": "Site web généré avec succès!"
}
```

### `GET /api/preview/{site_id}`
Prévisualise un site généré.

### `GET /api/download/{site_id}`
Télécharge un site en format ZIP.

### `GET /api/health`
Vérifie l'état du service.

## 🎨 Exemples de sites générés

Le générateur peut créer des sites pour tous types d'entreprises:

- 🍕 Restaurants et cafés
- 🏪 Commerces et boutiques
- 💼 Services professionnels
- 🏥 Cabinets médicaux
- 🎓 Écoles et formations
- 🏡 Agences immobilières
- 💻 Entreprises technologiques
- Et bien plus encore!

## 🌍 Support multi-langues

Sites disponibles en:
- 🇫🇷 Français
- 🇬🇧 Anglais
- 🇪🇸 Espagnol
- 🇩🇪 Allemand
- 🇮🇹 Italien

## 🔐 Sécurité

- Les clés API sont stockées dans des variables d'environnement
- Validation des entrées utilisateur avec Pydantic
- Protection CORS configurée
- Pas de stockage de données sensibles

## 🚧 Améliorations futures

- [ ] Support de plus de langues
- [ ] Système de templates personnalisables
- [ ] Génération d'images avec DALL-E
- [ ] Éditeur visuel intégré
- [ ] Hébergement automatique
- [ ] Intégration de CMS
- [ ] Génération de formulaires de contact fonctionnels
- [ ] Analytics intégré
- [ ] SEO avancé

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Ouvrir des issues pour signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.

## 💡 Inspiré par

Ce projet est inspiré par [ZipWP](https://zipwp.com/), un générateur de sites WordPress alimenté par l'IA.

## 📞 Support

Pour toute question ou problème:
- Ouvrir une issue sur GitHub
- Consulter la documentation de l'API Claude: https://docs.anthropic.com

## 🙏 Remerciements

- **Anthropic** pour l'API Claude AI
- **FastAPI** pour le framework web
- **ZipWP** pour l'inspiration

---

**Propulsé par Claude AI** 🤖 | **Créé avec ❤️**
