"""
AI Generator - Génération de contenu avec Claude API
"""

import anthropic
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AIWebsiteGenerator:
    """
    Générateur de sites web utilisant Claude AI
    """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    async def generate_site_structure(
        self,
        business_description: str,
        business_name: str,
        industry: Optional[str] = None,
        target_audience: Optional[str] = None,
        language: str = "fr",
        requested_pages: Optional[List[str]] = None
    ) -> Dict:
        """
        Générer la structure du site (pages, navigation, sections)
        """

        prompt = f"""Tu es un expert en architecture de sites web. Crée une structure de site web professionnelle et moderne pour l'entreprise suivante:

Nom de l'entreprise: {business_name}
Description: {business_description}
{f"Industrie: {industry}" if industry else ""}
{f"Public cible: {target_audience}" if target_audience else ""}
Langue: {language}

{f"Pages demandées: {', '.join(requested_pages)}" if requested_pages else ""}

Génère une structure de site web complète avec:
1. Une liste de pages recommandées (minimum 4-5 pages)
2. Les sections pour chaque page
3. La navigation du site
4. Les éléments clés à inclure

Réponds UNIQUEMENT avec un objet JSON valide dans ce format exact:
{{
    "pages": [
        {{
            "name": "Accueil",
            "slug": "index",
            "sections": ["hero", "services", "about", "testimonials", "cta"]
        }},
        {{
            "name": "À propos",
            "slug": "about",
            "sections": ["story", "team", "values"]
        }}
    ],
    "navigation": ["Accueil", "Services", "À propos", "Contact"],
    "recommended_features": ["Contact form", "Newsletter signup", "Social media links"]
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text

            # Extraire le JSON de la réponse
            structure = json.loads(response_text)
            logger.info(f"Structure générée: {len(structure.get('pages', []))} pages")

            return structure

        except Exception as e:
            logger.error(f"Erreur lors de la génération de la structure: {e}")
            # Structure par défaut en cas d'erreur
            return {
                "pages": [
                    {
                        "name": "Accueil",
                        "slug": "index",
                        "sections": ["hero", "services", "about", "contact"]
                    }
                ],
                "navigation": ["Accueil", "Services", "Contact"],
                "recommended_features": ["Contact form"]
            }

    async def generate_pages_content(
        self,
        site_structure: Dict,
        business_description: str,
        language: str = "fr"
    ) -> Dict[str, Dict]:
        """
        Générer le contenu pour chaque page du site
        """

        pages_content = {}

        for page in site_structure.get("pages", []):
            page_slug = page.get("slug", "page")
            page_name = page.get("name", "Page")
            sections = page.get("sections", [])

            logger.info(f"Génération du contenu pour: {page_name}")

            prompt = f"""Tu es un rédacteur web professionnel. Crée un contenu de qualité pour la page "{page_name}" d'un site web.

Contexte de l'entreprise: {business_description}
Langue: {language}
Sections à créer: {', '.join(sections)}

Pour chaque section, génère:
- Un titre accrocheur
- Un texte descriptif engageant et professionnel
- Des appels à l'action pertinents

Réponds UNIQUEMENT avec un objet JSON valide dans ce format:
{{
    "page_title": "Titre de la page",
    "meta_description": "Description SEO de 150-160 caractères",
    "sections": {{
        "hero": {{
            "title": "Titre principal",
            "subtitle": "Sous-titre",
            "cta_text": "Appel à l'action",
            "content": "Contenu de la section"
        }},
        "services": {{
            "title": "Nos Services",
            "items": [
                {{
                    "title": "Service 1",
                    "description": "Description du service"
                }}
            ]
        }}
    }}
}}"""

            try:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=3072,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                response_text = message.content[0].text
                content = json.loads(response_text)
                pages_content[page_slug] = content

            except Exception as e:
                logger.error(f"Erreur lors de la génération du contenu pour {page_name}: {e}")
                # Contenu par défaut
                pages_content[page_slug] = {
                    "page_title": page_name,
                    "meta_description": f"Page {page_name}",
                    "sections": {}
                }

        return pages_content

    async def generate_color_scheme(
        self,
        business_description: str,
        industry: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Générer un schéma de couleurs adapté à l'entreprise
        """

        prompt = f"""Tu es un designer web expert. Crée un schéma de couleurs professionnel et moderne pour:

Description: {business_description}
{f"Industrie: {industry}" if industry else ""}

Génère des couleurs harmonieuses adaptées à cette entreprise.

Réponds UNIQUEMENT avec un objet JSON valide:
{{
    "primary": "#hexcode",
    "secondary": "#hexcode",
    "accent": "#hexcode",
    "background": "#hexcode",
    "text": "#hexcode"
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            colors = json.loads(response_text)

            return colors

        except Exception as e:
            logger.error(f"Erreur lors de la génération des couleurs: {e}")
            # Schéma par défaut
            return {
                "primary": "#2563eb",
                "secondary": "#7c3aed",
                "accent": "#f59e0b",
                "background": "#ffffff",
                "text": "#1f2937"
            }
