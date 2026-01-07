"""
AI Website Generator - Backend API
Générateur de sites web automatisé avec IA
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import logging

from ai_generator import AIWebsiteGenerator
from website_builder import WebsiteBuilder

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialisation de l'application FastAPI
app = FastAPI(
    title="AI Website Generator",
    description="Service de génération automatisée de sites web avec IA",
    version="1.0.0"
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
website_builder = WebsiteBuilder()


# Modèles de données
class WebsiteRequest(BaseModel):
    business_description: str
    business_name: str
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    language: str = "fr"
    color_scheme: Optional[str] = None
    pages: Optional[List[str]] = None


class WebsiteResponse(BaseModel):
    site_id: str
    preview_url: str
    download_url: str
    pages: List[str]
    message: str


@app.get("/")
async def root():
    """Servir la page d'accueil"""
    return FileResponse("frontend/index.html")


@app.post("/api/generate", response_model=WebsiteResponse)
async def generate_website(request: WebsiteRequest):
    """
    Générer un site web complet à partir d'une description
    """
    try:
        logger.info(f"Génération d'un site pour: {request.business_name}")

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

        # Étape 4: Construire le site web (HTML/CSS/JS)
        logger.info("Construction des fichiers du site...")
        site_id = website_builder.build_website(
            business_name=request.business_name,
            site_structure=site_structure,
            pages_content=pages_content,
            color_scheme=color_scheme
        )

        logger.info(f"Site généré avec succès: {site_id}")

        return WebsiteResponse(
            site_id=site_id,
            preview_url=f"/api/preview/{site_id}",
            download_url=f"/api/download/{site_id}",
            pages=list(pages_content.keys()),
            message=f"Site web généré avec succès pour {request.business_name}!"
        )

    except Exception as e:
        logger.error(f"Erreur lors de la génération: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/preview/{site_id}")
async def preview_site(site_id: str):
    """
    Prévisualiser un site généré
    """
    site_path = f"generated_sites/{site_id}/index.html"

    if not os.path.exists(site_path):
        raise HTTPException(status_code=404, detail="Site non trouvé")

    return FileResponse(site_path)


@app.get("/api/download/{site_id}")
async def download_site(site_id: str):
    """
    Télécharger un site généré en ZIP
    """
    import shutil

    site_dir = f"generated_sites/{site_id}"

    if not os.path.exists(site_dir):
        raise HTTPException(status_code=404, detail="Site non trouvé")

    # Créer une archive ZIP
    zip_path = f"generated_sites/{site_id}.zip"
    shutil.make_archive(f"generated_sites/{site_id}", 'zip', site_dir)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{site_id}.zip"
    )


@app.get("/api/health")
async def health_check():
    """
    Vérifier l'état du service
    """
    return {
        "status": "healthy",
        "service": "AI Website Generator",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    logger.info(f"Démarrage du serveur sur {host}:{port}")
    uvicorn.run(app, host=host, port=port)
