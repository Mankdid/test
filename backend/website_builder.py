"""
Website Builder - Construction des fichiers HTML/CSS/JS
"""

import os
import uuid
import logging
from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


class WebsiteBuilder:
    """
    Constructeur de sites web à partir de templates
    """

    def __init__(self):
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs("generated_sites", exist_ok=True)

        # Configurer Jinja2
        self.env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def build_website(
        self,
        business_name: str,
        site_structure: Dict,
        pages_content: Dict[str, Dict],
        color_scheme: Dict[str, str]
    ) -> str:
        """
        Construire le site web complet
        """

        # Générer un ID unique pour le site
        site_id = f"{business_name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
        site_dir = f"generated_sites/{site_id}"

        # Créer la structure de dossiers
        os.makedirs(site_dir, exist_ok=True)
        os.makedirs(f"{site_dir}/css", exist_ok=True)
        os.makedirs(f"{site_dir}/js", exist_ok=True)
        os.makedirs(f"{site_dir}/images", exist_ok=True)

        logger.info(f"Construction du site dans: {site_dir}")

        # Générer le fichier CSS principal
        self._generate_css(site_dir, color_scheme)

        # Générer le fichier JS
        self._generate_js(site_dir)

        # Générer chaque page HTML
        for page in site_structure.get("pages", []):
            page_slug = page.get("slug", "page")
            page_content = pages_content.get(page_slug, {})

            self._generate_html_page(
                site_dir=site_dir,
                page_slug=page_slug,
                page_data=page,
                page_content=page_content,
                navigation=site_structure.get("navigation", []),
                business_name=business_name
            )

        logger.info(f"Site construit avec succès: {site_id}")
        return site_id

    def _generate_css(self, site_dir: str, colors: Dict[str, str]):
        """
        Générer le fichier CSS avec le schéma de couleurs
        """

        css_content = f"""/* AI Generated Website - Styles */
:root {{
    --color-primary: {colors.get('primary', '#2563eb')};
    --color-secondary: {colors.get('secondary', '#7c3aed')};
    --color-accent: {colors.get('accent', '#f59e0b')};
    --color-background: {colors.get('background', '#ffffff')};
    --color-text: {colors.get('text', '#1f2937')};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--color-text);
    background-color: var(--color-background);
}}

/* Navigation */
nav {{
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    padding: 1rem 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}}

nav .container {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

nav .logo {{
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}}

nav ul {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}}

nav a:hover {{
    opacity: 0.8;
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    padding: 6rem 2rem;
    text-align: center;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease;
}}

.hero p {{
    font-size: 1.25rem;
    margin-bottom: 2rem;
    animation: fadeInUp 1s ease 0.2s both;
}}

/* Container */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Sections */
section {{
    padding: 4rem 2rem;
}}

section h2 {{
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    color: var(--color-primary);
}}

/* Cards */
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.card {{
    background: white;
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0,0,0,0.15);
}}

.card h3 {{
    color: var(--color-primary);
    margin-bottom: 1rem;
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 1rem 2rem;
    background: var(--color-accent);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: transform 0.3s, box-shadow 0.3s;
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}}

.btn-primary {{
    background: var(--color-primary);
}}

.btn-secondary {{
    background: var(--color-secondary);
}}

/* Footer */
footer {{
    background: var(--color-text);
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 4rem;
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive */
@media (max-width: 768px) {{
    nav ul {{
        flex-direction: column;
        gap: 1rem;
    }}

    .hero h1 {{
        font-size: 2rem;
    }}

    section h2 {{
        font-size: 2rem;
    }}
}}
"""

        with open(f"{site_dir}/css/style.css", "w", encoding="utf-8") as f:
            f.write(css_content)

    def _generate_js(self, site_dir: str):
        """
        Générer le fichier JavaScript
        """

        js_content = """// AI Generated Website - Scripts

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 1s ease';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, section').forEach(el => {
        observer.observe(el);
    });
});
"""

        with open(f"{site_dir}/js/script.js", "w", encoding="utf-8") as f:
            f.write(js_content)

    def _generate_html_page(
        self,
        site_dir: str,
        page_slug: str,
        page_data: Dict,
        page_content: Dict,
        navigation: list,
        business_name: str
    ):
        """
        Générer une page HTML
        """

        filename = f"{page_slug}.html"
        page_title = page_content.get("page_title", page_data.get("name", "Page"))
        meta_description = page_content.get("meta_description", "")
        sections = page_content.get("sections", {})

        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_description}">
    <title>{page_title} - {business_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav>
        <div class="container">
            <a href="index.html" class="logo">{business_name}</a>
            <ul>
"""

        # Ajouter la navigation
        for nav_item in navigation:
            nav_slug = nav_item.lower().replace(" ", "-").replace("à", "a")
            if nav_slug == "accueil":
                nav_slug = "index"
            html_content += f'                <li><a href="{nav_slug}.html">{nav_item}</a></li>\n'

        html_content += """            </ul>
        </div>
    </nav>

"""

        # Générer les sections
        for section_name, section_data in sections.items():
            if section_name == "hero":
                html_content += self._generate_hero_section(section_data)
            elif section_name == "services" or "items" in section_data:
                html_content += self._generate_cards_section(section_data)
            else:
                html_content += self._generate_text_section(section_data)

        # Footer
        html_content += f"""
    <footer>
        <div class="container">
            <p>&copy; 2026 {business_name}. Tous droits réservés.</p>
            <p>Site généré automatiquement par AI Website Generator</p>
        </div>
    </footer>

    <script src="js/script.js"></script>
</body>
</html>
"""

        with open(f"{site_dir}/{filename}", "w", encoding="utf-8") as f:
            f.write(html_content)

    def _generate_hero_section(self, data: Dict) -> str:
        """Générer une section hero"""
        return f"""    <section class="hero">
        <div class="container">
            <h1>{data.get('title', '')}</h1>
            <p>{data.get('subtitle', '')}</p>
            <a href="#contact" class="btn btn-primary">{data.get('cta_text', 'Contactez-nous')}</a>
        </div>
    </section>

"""

    def _generate_cards_section(self, data: Dict) -> str:
        """Générer une section avec des cartes"""
        html = f"""    <section>
        <div class="container">
            <h2>{data.get('title', '')}</h2>
            <div class="cards">
"""

        for item in data.get('items', []):
            html += f"""                <div class="card">
                    <h3>{item.get('title', '')}</h3>
                    <p>{item.get('description', '')}</p>
                </div>
"""

        html += """            </div>
        </div>
    </section>

"""
        return html

    def _generate_text_section(self, data: Dict) -> str:
        """Générer une section de texte"""
        return f"""    <section>
        <div class="container">
            <h2>{data.get('title', '')}</h2>
            <p>{data.get('content', '')}</p>
        </div>
    </section>

"""
