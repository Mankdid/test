# 🚀 AI WordPress Template Generator

Un service de génération automatisée de templates WordPress professionnels avec l'Intelligence Artificielle, optimisé pour le thème Astra.

## 📋 Description

AI WordPress Template Generator est un outil puissant qui permet de créer des templates WordPress complets et professionnels en moins de 60 secondes. Propulsé par Claude AI d'Anthropic, il génère automatiquement:

- 🏗️ **Templates WordPress** prêts à importer
- ✍️ **Contenu professionnel** (textes SEO-optimisés)
- 🎨 **Configuration Astra** (thème WordPress léger et rapide)
- 🧱 **Blocs Spectra** (constructeur de blocs WordPress)
- 🌈 **Schémas de couleurs** adaptés à votre secteur
- 📱 **Sites mobile-friendly**
- 🌍 **Support multi-langues**
- 📦 **Blueprints réutilisables** pour gagner du temps

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

### Export WordPress
- Format WXR (WordPress eXtended RSS)
- Configuration Astra incluse
- Blocs Spectra personnalisés
- Import en un clic dans WordPress
- Blueprints sauvegardables et réutilisables

## 🛠️ Technologies utilisées

### Backend
- **FastAPI** - Framework web moderne et performant
- **Python 3.8+**
- **Anthropic Claude API** - Intelligence artificielle
- **Jinja2** - Moteur de templates
- **Pydantic** - Validation des données

### WordPress Integration
- **Astra Theme** - Thème WordPress léger et performant
- **Spectra Blocks** - Constructeur de blocs WordPress
- **WXR Format** - Export/Import WordPress standard
- **Gutenberg Blocks** - Éditeur de blocs natif

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
mkdir -p generated_templates templates blueprints
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
3. Cliquer sur "Générer mon template WordPress"
4. Attendre ~60 secondes
5. Télécharger le fichier WXR et les fichiers de configuration
6. Importer dans WordPress (Outils > Importer > WordPress)
7. Activer le thème Astra et appliquer la configuration!

## 📁 Structure du projet

```
test/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # API FastAPI principale
│   ├── ai_generator.py            # Génération de contenu IA
│   ├── wordpress_generator.py     # Génération WordPress/WXR
│   ├── astra_configurator.py      # Configuration du thème Astra
│   ├── spectra_builder.py         # Constructeur de blocs Spectra
│   └── blueprint_manager.py       # Gestion des blueprints
├── frontend/
│   ├── index.html                 # Interface utilisateur
│   ├── style.css                  # Styles
│   └── script.js                  # Logique frontend
├── templates/                     # Templates de base
├── blueprints/                    # Blueprints réutilisables
├── generated_templates/           # Templates WordPress générés
├── requirements.txt               # Dépendances Python
├── .env.example                   # Variables d'environnement exemple
├── .gitignore
└── README.md
```

## 🔧 API Endpoints

### `POST /api/generate`
Génère un template WordPress complet avec configuration Astra.

**Corps de la requête:**
```json
{
  "business_name": "Mon Entreprise",
  "business_description": "Description de l'activité...",
  "industry": "technology",
  "target_audience": "Professionnels",
  "language": "fr",
  "pages": ["Accueil", "Services", "Contact"],
  "save_as_blueprint": false
}
```

**Réponse:**
```json
{
  "template_id": "mon-entreprise-abc123",
  "download_url": "/api/download/mon-entreprise-abc123",
  "files": {
    "wxr": "template.xml",
    "astra_config": "astra-settings.json",
    "spectra_blocks": "spectra-blocks.json"
  },
  "pages": ["accueil", "services", "contact"],
  "message": "Template WordPress généré avec succès!"
}
```

### `GET /api/download/{template_id}`
Télécharge le template WordPress complet en ZIP.

### `POST /api/blueprints/save`
Sauvegarde un template comme blueprint réutilisable.

### `GET /api/blueprints/list`
Liste tous les blueprints disponibles.

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
- [ ] Plus de variations de blocs Spectra
- [ ] Génération d'images avec DALL-E
- [ ] Intégration WooCommerce pour sites e-commerce
- [ ] Support d'autres page builders (Elementor, Beaver Builder)
- [ ] Génération de formulaires Contact Form 7
- [ ] Export vers WordPress.com et WP Engine
- [ ] Optimisation SEO automatique (Yoast/RankMath)
- [ ] Génération de contenus de blog
- [ ] Templates pour custom post types

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Ouvrir des issues pour signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou problème:
- Ouvrir une issue sur GitHub
- Consulter la documentation de l'API Claude: https://docs.anthropic.com
- Documentation WordPress: https://wordpress.org/documentation/
- Documentation Astra: https://wpastra.com/docs/

## 🙏 Remerciements

- **Anthropic** pour l'API Claude AI
- **FastAPI** pour le framework web
- **Astra Team** pour le thème WordPress
- **Spectra Team** pour le constructeur de blocs
- La communauté **WordPress** pour l'écosystème open-source

---

**Propulsé par Claude AI** 🤖 | **Créé avec ❤️**
