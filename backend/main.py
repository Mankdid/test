"""
AI WordPress Template Generator - Backend API
Générateur de templates WordPress automatisé avec IA et thème Astra
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import shutil
from dotenv import load_dotenv
import logging

from ai_generator import AIWebsiteGenerator
from wordpress_generator import WordPressGenerator
from astra_configurator import AstraConfigurator
from spectra_builder import SpectraBuilder
from blueprint_manager import BlueprintManager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialisation de l'application FastAPI
app = FastAPI(
    title="AI WordPress Template Generator",
    description="Service de génération automatisée de templates WordPress avec Astra",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter le dossier frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialiser les services
ai_generator = AIWebsiteGenerator(api_key=os.getenv("ANTHROPIC_API_KEY"))
wordpress_generator = WordPressGenerator()
astra_configurator = AstraConfigurator()
spectra_builder = SpectraBuilder()
blueprint_manager = BlueprintManager()


# Modèles de données
class WordPressTemplateRequest(BaseModel):
    business_description: str
    business_name: str
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    language: str = "fr"
    color_scheme: Optional[str] = None
    pages: Optional[List[str]] = None
    save_as_blueprint: bool = False
    blueprint_name: Optional[str] = None


class WordPressTemplateResponse(BaseModel):
    template_id: str
    download_url: str
    files: Dict[str, str]
    pages: List[str]
    message: str
    blueprint_id: Optional[str] = None


@app.get("/")
async def root():
    """Servir la page d'accueil"""
    return FileResponse("frontend/index.html")


@app.post("/api/generate", response_model=WordPressTemplateResponse)
async def generate_wordpress_template(request: WordPressTemplateRequest):
    """
    Générer un template WordPress complet avec configuration Astra
    """
    try:
        logger.info(f"Génération d'un template WordPress pour: {request.business_name}")

        # Étape 1: Générer la structure et le contenu avec l'IA
        logger.info("Génération de la structure du site...")
        site_structure = await ai_generator.generate_site_structure(
            business_description=request.business_description,
            business_name=request.business_name,
            industry=request.industry,
            target_audience=request.target_audience,
            language=request.language,
            requested_pages=request.pages
        )

        # Étape 2: Générer le contenu pour chaque page
        logger.info("Génération du contenu des pages...")
        pages_content = await ai_generator.generate_pages_content(
            site_structure=site_structure,
            business_description=request.business_description,
            language=request.language
        )

        # Étape 3: Générer le schéma de couleurs si non fourni
        if not request.color_scheme:
            logger.info("Génération du schéma de couleurs...")
            color_scheme = await ai_generator.generate_color_scheme(
                business_description=request.business_description,
                industry=request.industry
            )
        else:
            color_scheme = request.color_scheme

        # Étape 4: Générer le fichier WXR WordPress
        logger.info("Génération du fichier WXR WordPress...")
        wxr_content = wordpress_generator.generate_wxr(
            business_name=request.business_name,
            site_structure=site_structure,
            pages_content=pages_content,
            language=f"{request.language}-{request.language.upper()}"
        )

        # Étape 5: Générer la configuration Astra
        logger.info("Génération de la configuration Astra...")
        astra_config = astra_configurator.generate_astra_config(
            business_name=request.business_name,
            color_scheme=color_scheme,
            site_structure=site_structure
        )

        astra_json = astra_configurator.export_to_json(astra_config)
        astra_css = astra_configurator.generate_custom_css(color_scheme)

        # Étape 6: Générer les blocs Spectra
        logger.info("Génération des blocs Spectra...")
        spectra_blocks = spectra_builder.generate_spectra_blocks(
            pages_content=pages_content,
            color_scheme=color_scheme
        )

        spectra_json = spectra_builder.export_to_json(spectra_blocks)

        # Étape 7: Créer la structure de dossiers et sauvegarder les fichiers
        template_id = f"{request.business_name.lower().replace(' ', '-')}-{os.urandom(4).hex()}"
        template_dir = f"generated_templates/{template_id}"

        os.makedirs(template_dir, exist_ok=True)

        # Sauvegarder tous les fichiers
        files = {
            "wxr": "wordpress-export.xml",
            "astra_config": "astra-settings.json",
            "astra_css": "astra-custom.css",
            "spectra_blocks": "spectra-blocks.json",
            "readme": "README.txt"
        }

        with open(f"{template_dir}/{files['wxr']}", "w", encoding="utf-8") as f:
            f.write(wxr_content)

        with open(f"{template_dir}/{files['astra_config']}", "w", encoding="utf-8") as f:
            f.write(astra_json)

        with open(f"{template_dir}/{files['astra_css']}", "w", encoding="utf-8") as f:
            f.write(astra_css)

        with open(f"{template_dir}/{files['spectra_blocks']}", "w", encoding="utf-8") as f:
            f.write(spectra_json)

        # Créer un fichier README avec les instructions
        readme_content = f"""Template WordPress pour {request.business_name}
========================================

Généré automatiquement par AI WordPress Template Generator

Fichiers inclus:
- {files['wxr']}: Fichier d'export WordPress à importer
- {files['astra_config']}: Configuration du thème Astra
- {files['astra_css']}: CSS personnalisé pour Astra
- {files['spectra_blocks']}: Configuration des blocs Spectra

Instructions d'installation:
1. Installer WordPress sur votre serveur
2. Installer et activer le thème Astra
3. Installer et activer le plugin Spectra (Ultimate Addons for Gutenberg)
4. Aller dans Outils > Importer > WordPress
5. Importer le fichier {files['wxr']}
6. Aller dans Apparence > Personnaliser > Astra
7. Importer le fichier {files['astra_config']}
8. Ajouter le CSS personnalisé depuis {files['astra_css']}
9. Votre site est prêt!

Pages générées: {', '.join([page.get('name', '') for page in site_structure.get('pages', [])])}

Support:
- Documentation WordPress: https://wordpress.org/documentation/
- Documentation Astra: https://wpastra.com/docs/
- Documentation Spectra: https://wpspectra.com/docs/
"""

        with open(f"{template_dir}/{files['readme']}", "w", encoding="utf-8") as f:
            f.write(readme_content)

        # Étape 8: Sauvegarder comme blueprint si demandé
        blueprint_id = None
        if request.save_as_blueprint:
            blueprint_name = request.blueprint_name or request.business_name
            blueprint_id = blueprint_manager.save_blueprint(
                template_id=template_id,
                business_name=blueprint_name,
                site_structure=site_structure,
                pages_content=pages_content,
                color_scheme=color_scheme,
                astra_config=astra_config,
                spectra_blocks=spectra_blocks,
                metadata={
                    "industry": request.industry,
                    "language": request.language,
                    "pages_count": len(site_structure.get("pages", []))
                }
            )
            logger.info(f"Template sauvegardé comme blueprint: {blueprint_id}")

        logger.info(f"Template WordPress généré avec succès: {template_id}")

        return WordPressTemplateResponse(
            template_id=template_id,
            download_url=f"/api/download/{template_id}",
            files=files,
            pages=[page.get("slug", "") for page in site_structure.get("pages", [])],
            message=f"Template WordPress généré avec succès pour {request.business_name}!",
            blueprint_id=blueprint_id
        )

    except Exception as e:
        logger.error(f"Erreur lors de la génération: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{template_id}")
async def download_template(template_id: str):
    """
    Télécharger un template WordPress en ZIP
    """
    template_dir = f"generated_templates/{template_id}"

    if not os.path.exists(template_dir):
        raise HTTPException(status_code=404, detail="Template non trouvé")

    # Créer une archive ZIP
    zip_path = f"generated_templates/{template_id}"
    shutil.make_archive(zip_path, 'zip', template_dir)

    return FileResponse(
        f"{zip_path}.zip",
        media_type="application/zip",
        filename=f"wordpress-template-{template_id}.zip"
    )


@app.post("/api/blueprints/save")
async def save_blueprint(template_id: str, blueprint_name: str):
    """
    Sauvegarder un template comme blueprint
    """
    # Cette route pourrait être utilisée pour sauvegarder un template après génération
    return {"message": "Blueprint sauvegardé", "blueprint_id": f"blueprint-{template_id}"}


@app.get("/api/blueprints/list")
async def list_blueprints():
    """
    Lister tous les blueprints disponibles
    """
    blueprints = blueprint_manager.list_blueprints()

    return {
        "blueprints": blueprints,
        "total": len(blueprints)
    }


@app.get("/api/blueprints/{blueprint_id}")
async def get_blueprint(blueprint_id: str):
    """
    Obtenir les détails d'un blueprint
    """
    blueprint = blueprint_manager.load_blueprint(blueprint_id)

    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint non trouvé")

    return blueprint


@app.delete("/api/blueprints/{blueprint_id}")
async def delete_blueprint(blueprint_id: str):
    """
    Supprimer un blueprint
    """
    success = blueprint_manager.delete_blueprint(blueprint_id)

    if not success:
        raise HTTPException(status_code=404, detail="Blueprint non trouvé")

    return {"message": "Blueprint supprimé avec succès"}


@app.get("/api/health")
async def health_check():
    """
    Vérifier l'état du service
    """
    return {
        "status": "healthy",
        "service": "AI WordPress Template Generator",
        "version": "2.0.0",
        "features": ["WordPress WXR", "Astra Theme", "Spectra Blocks", "Blueprints"]
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    # Créer les dossiers nécessaires
    os.makedirs("generated_templates", exist_ok=True)
    os.makedirs("blueprints", exist_ok=True)

    logger.info(f"Démarrage du serveur sur {host}:{port}")
    uvicorn.run(app, host=host, port=port)
