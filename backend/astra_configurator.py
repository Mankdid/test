"""
Astra Theme Configurator - Configuration du thème Astra pour WordPress
"""

import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class AstraConfigurator:
    """
    Générateur de configuration pour le thème Astra
    """

    def __init__(self):
        self.version = "4.0.0"

    def generate_astra_config(
        self,
        business_name: str,
        color_scheme: Dict[str, str],
        site_structure: Dict
    ) -> Dict:
        """
        Générer la configuration complète du thème Astra
        """

        config = {
            "astra-settings": {
                # Informations générales
                "site-identity": {
                    "site-title": business_name,
                    "site-tagline": f"Site professionnel de {business_name}"
                },

                # Couleurs globales
                "colors": {
                    "theme-color": color_scheme.get("primary", "#2563eb"),
                    "link-color": color_scheme.get("primary", "#2563eb"),
                    "text-color": color_scheme.get("text", "#1f2937"),
                    "heading-base-color": color_scheme.get("text", "#1f2937"),
                    "border-color": "#e2e8f0"
                },

                # Typographie
                "typography": {
                    "body-font-family": "system-ui, -apple-system, sans-serif",
                    "body-font-weight": "400",
                    "body-line-height": "1.6",
                    "body-font-size": {
                        "desktop": "16",
                        "tablet": "15",
                        "mobile": "15",
                        "desktop-unit": "px",
                        "tablet-unit": "px",
                        "mobile-unit": "px"
                    },
                    "headings-font-family": "system-ui, -apple-system, sans-serif",
                    "headings-font-weight": "600"
                },

                # Header
                "header": {
                    "header-main-layout": "header-main-layout-1",
                    "header-bg-obj": {
                        "background-color": "#ffffff",
                        "background-type": "color"
                    },
                    "primary-menu-color": color_scheme.get("text", "#1f2937"),
                    "primary-menu-h-color": color_scheme.get("primary", "#2563eb"),
                    "header-spacing": {
                        "desktop": {
                            "top": "20",
                            "right": "20",
                            "bottom": "20",
                            "left": "20"
                        }
                    },
                    "sticky-header-enable": True
                },

                # Footer
                "footer": {
                    "footer-bg-obj": {
                        "background-color": color_scheme.get("text", "#1f2937"),
                        "background-type": "color"
                    },
                    "footer-color": "#ffffff",
                    "footer-link-color": "#ffffff",
                    "footer-adv": "layout-4",
                    "footer-copyright-text": f"© 2026 {business_name}. Tous droits réservés."
                },

                # Sidebar
                "sidebar": {
                    "site-sidebar-layout": "no-sidebar",
                    "single-page-sidebar-layout": "no-sidebar"
                },

                # Container
                "container": {
                    "site-content-layout": "content-boxed-container",
                    "site-content-width": 1200
                },

                # Boutons
                "buttons": {
                    "button-color": "#ffffff",
                    "button-h-color": "#ffffff",
                    "button-bg-color": color_scheme.get("accent", "#f59e0b"),
                    "button-bg-h-color": color_scheme.get("primary", "#2563eb"),
                    "button-border-radius": 5,
                    "button-padding": {
                        "desktop": {
                            "top": "12",
                            "right": "24",
                            "bottom": "12",
                            "left": "24"
                        }
                    }
                },

                # Performance
                "performance": {
                    "disable-emoji": True,
                    "fast-google-fonts": True
                },

                # Blog
                "blog": {
                    "blog-layout": "blog-layout-1",
                    "blog-post-structure": ["title-meta", "image", "excerpt"],
                    "blog-grid": 3
                }
            },

            # Customizer settings
            "theme-mods": {
                "custom_logo": "",
                "header_textcolor": color_scheme.get("text", "#1f2937").replace("#", ""),
                "background_color": "#ffffff"
            }
        }

        logger.info("Configuration Astra générée avec succès")

        return config

    def export_to_json(self, config: Dict) -> str:
        """
        Exporter la configuration en JSON
        """

        return json.dumps(config, indent=2, ensure_ascii=False)

    def generate_custom_css(self, color_scheme: Dict[str, str]) -> str:
        """
        Générer du CSS personnalisé pour Astra
        """

        css = f"""
/* Custom CSS for Astra Theme */
:root {{
    --ast-global-color-0: {color_scheme.get('primary', '#2563eb')};
    --ast-global-color-1: {color_scheme.get('secondary', '#7c3aed')};
    --ast-global-color-2: {color_scheme.get('accent', '#f59e0b')};
    --ast-global-color-3: {color_scheme.get('text', '#1f2937')};
    --ast-global-color-4: {color_scheme.get('background', '#ffffff')};
}}

/* Hero Section Styling */
.wp-block-cover {{
    min-height: 500px;
}}

/* Button Hover Effects */
.wp-block-button__link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}}

/* Columns Responsive */
@media (max-width: 768px) {{
    .wp-block-columns {{
        flex-direction: column;
    }}
}}

/* Smooth Scrolling */
html {{
    scroll-behavior: smooth;
}}

/* Card Style for Columns */
.wp-block-column {{
    padding: 2rem;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}}

.wp-block-column:hover {{
    transform: translateY(-5px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}}

/* Heading Styling */
h1, h2, h3 {{
    font-weight: 600;
}}

h2 {{
    margin-bottom: 2rem;
}}

/* Section Spacing */
.wp-block-group {{
    padding: 4rem 2rem;
}}
"""

        return css.strip()

    def generate_global_palette(self, color_scheme: Dict[str, str]) -> Dict:
        """
        Générer la palette de couleurs globale pour Astra
        """

        palette = {
            "palette": [
                {
                    "slug": "primary",
                    "color": color_scheme.get("primary", "#2563eb"),
                    "name": "Primary"
                },
                {
                    "slug": "secondary",
                    "color": color_scheme.get("secondary", "#7c3aed"),
                    "name": "Secondary"
                },
                {
                    "slug": "accent",
                    "color": color_scheme.get("accent", "#f59e0b"),
                    "name": "Accent"
                },
                {
                    "slug": "text",
                    "color": color_scheme.get("text", "#1f2937"),
                    "name": "Text"
                },
                {
                    "slug": "background",
                    "color": color_scheme.get("background", "#ffffff"),
                    "name": "Background"
                }
            ]
        }

        return palette
