"""
Spectra Block Builder - Génération de blocs Spectra pour WordPress
"""

import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class SpectraBuilder:
    """
    Constructeur de blocs Spectra (anciennement UAG - Ultimate Addons for Gutenberg)
    """

    def __init__(self):
        self.version = "2.0.0"

    def generate_spectra_blocks(
        self,
        pages_content: Dict[str, Dict],
        color_scheme: Dict[str, str]
    ) -> Dict:
        """
        Générer la configuration des blocs Spectra
        """

        blocks_config = {
            "version": self.version,
            "blocks": [],
            "global_settings": self._generate_global_settings(color_scheme)
        }

        # Générer les blocs pour chaque page
        for page_slug, page_content in pages_content.items():
            page_blocks = self._generate_page_blocks(page_content, color_scheme)
            blocks_config["blocks"].extend(page_blocks)

        logger.info(f"Configuration Spectra générée avec {len(blocks_config['blocks'])} blocs")

        return blocks_config

    def _generate_global_settings(self, color_scheme: Dict[str, str]) -> Dict:
        """
        Générer les paramètres globaux des blocs Spectra
        """

        return {
            "colors": {
                "primary": color_scheme.get("primary", "#2563eb"),
                "secondary": color_scheme.get("secondary", "#7c3aed"),
                "accent": color_scheme.get("accent", "#f59e0b")
            },
            "typography": {
                "font_family": "system-ui, -apple-system, sans-serif",
                "font_size": {
                    "desktop": 16,
                    "tablet": 15,
                    "mobile": 14
                }
            },
            "spacing": {
                "padding": {
                    "desktop": 40,
                    "tablet": 30,
                    "mobile": 20
                }
            }
        }

    def _generate_page_blocks(
        self,
        page_content: Dict,
        color_scheme: Dict[str, str]
    ) -> List[Dict]:
        """
        Générer les blocs pour une page
        """

        blocks = []
        sections = page_content.get("sections", {})

        for section_name, section_data in sections.items():
            if section_name == "hero":
                blocks.append(self._create_hero_block(section_data, color_scheme))
            elif section_name == "services" or "items" in section_data:
                blocks.append(self._create_info_box_grid(section_data, color_scheme))
            elif section_name == "testimonials":
                blocks.append(self._create_testimonial_block(section_data, color_scheme))
            elif section_name == "cta":
                blocks.append(self._create_cta_block(section_data, color_scheme))
            else:
                blocks.append(self._create_content_block(section_data, color_scheme))

        return blocks

    def _create_hero_block(self, data: Dict, color_scheme: Dict[str, str]) -> Dict:
        """
        Créer un bloc hero Spectra (Container Block)
        """

        return {
            "blockName": "uagb/container",
            "attrs": {
                "block_id": self._generate_block_id(),
                "className": "hero-section",
                "backgroundType": "gradient",
                "backgroundGradient": {
                    "color1": color_scheme.get("primary", "#2563eb"),
                    "color2": color_scheme.get("secondary", "#7c3aed"),
                    "angle": 135
                },
                "contentPadding": {
                    "top": 100,
                    "bottom": 100,
                    "left": 20,
                    "right": 20
                },
                "textAlign": "center"
            },
            "innerBlocks": [
                {
                    "blockName": "uagb/heading",
                    "attrs": {
                        "headingTitle": data.get("title", ""),
                        "headingTag": "h1",
                        "headingColor": "#ffffff",
                        "headingFontSize": {
                            "desktop": 48,
                            "tablet": 36,
                            "mobile": 28
                        },
                        "headingFontWeight": "600"
                    }
                },
                {
                    "blockName": "uagb/heading",
                    "attrs": {
                        "headingTitle": data.get("subtitle", ""),
                        "headingTag": "p",
                        "headingColor": "#ffffff",
                        "headingFontSize": {
                            "desktop": 20,
                            "tablet": 18,
                            "mobile": 16
                        }
                    }
                },
                {
                    "blockName": "uagb/buttons",
                    "attrs": {
                        "buttons": [
                            {
                                "label": data.get("cta_text", "En savoir plus"),
                                "link": "#contact",
                                "backgroundColor": color_scheme.get("accent", "#f59e0b"),
                                "textColor": "#ffffff",
                                "borderRadius": 5,
                                "paddingTop": 15,
                                "paddingBottom": 15,
                                "paddingLeft": 30,
                                "paddingRight": 30
                            }
                        ]
                    }
                }
            ]
        }

    def _create_info_box_grid(self, data: Dict, color_scheme: Dict[str, str]) -> Dict:
        """
        Créer une grille de blocs Info Box
        """

        items = data.get("items", [])

        inner_blocks = []
        for item in items:
            inner_blocks.append({
                "blockName": "uagb/info-box",
                "attrs": {
                    "block_id": self._generate_block_id(),
                    "headingTitle": item.get("title", ""),
                    "headingDesc": item.get("description", ""),
                    "iconSize": 40,
                    "iconColor": color_scheme.get("primary", "#2563eb"),
                    "headingColor": color_scheme.get("text", "#1f2937"),
                    "descColor": color_scheme.get("text", "#64748b"),
                    "contentPadding": 30,
                    "backgroundColor": "#ffffff",
                    "borderRadius": 10,
                    "boxShadow": {
                        "enabled": True,
                        "horizontal": 0,
                        "vertical": 4,
                        "blur": 12,
                        "spread": 0,
                        "color": "rgba(0,0,0,0.1)"
                    },
                    "hoverEffect": "lift"
                }
            })

        return {
            "blockName": "uagb/container",
            "attrs": {
                "block_id": self._generate_block_id(),
                "className": "info-box-section",
                "contentPadding": {
                    "top": 60,
                    "bottom": 60,
                    "left": 20,
                    "right": 20
                }
            },
            "innerBlocks": [
                {
                    "blockName": "uagb/heading",
                    "attrs": {
                        "headingTitle": data.get("title", ""),
                        "headingTag": "h2",
                        "headingAlign": "center",
                        "headingColor": color_scheme.get("primary", "#2563eb"),
                        "headingFontSize": {
                            "desktop": 36,
                            "tablet": 30,
                            "mobile": 24
                        }
                    }
                },
                {
                    "blockName": "uagb/columns",
                    "attrs": {
                        "columns": min(len(items), 3),
                        "columnGap": 30
                    },
                    "innerBlocks": inner_blocks
                }
            ]
        }

    def _create_testimonial_block(self, data: Dict, color_scheme: Dict[str, str]) -> Dict:
        """
        Créer un bloc de témoignages
        """

        testimonials = data.get("items", [])

        return {
            "blockName": "uagb/testimonial",
            "attrs": {
                "block_id": self._generate_block_id(),
                "testimonialBlock": [
                    {
                        "description": item.get("content", ""),
                        "name": item.get("author", ""),
                        "company": item.get("company", ""),
                        "image": ""
                    }
                    for item in testimonials
                ],
                "columns": min(len(testimonials), 2),
                "backgroundColor": color_scheme.get("background", "#f8fafc"),
                "borderRadius": 10,
                "padding": 30
            }
        }

    def _create_cta_block(self, data: Dict, color_scheme: Dict[str, str]) -> Dict:
        """
        Créer un bloc Call-to-Action
        """

        return {
            "blockName": "uagb/call-to-action",
            "attrs": {
                "block_id": self._generate_block_id(),
                "ctaTitle": data.get("title", ""),
                "ctaText": data.get("content", ""),
                "ctaButtonText": data.get("button_text", "Contactez-nous"),
                "ctaLink": data.get("button_link", "#contact"),
                "backgroundType": "color",
                "backgroundColor": color_scheme.get("primary", "#2563eb"),
                "titleColor": "#ffffff",
                "textColor": "#ffffff",
                "buttonColor": color_scheme.get("accent", "#f59e0b"),
                "buttonTextColor": "#ffffff",
                "contentPadding": {
                    "top": 60,
                    "bottom": 60,
                    "left": 30,
                    "right": 30
                },
                "borderRadius": 10
            }
        }

    def _create_content_block(self, data: Dict, color_scheme: Dict[str, str]) -> Dict:
        """
        Créer un bloc de contenu simple
        """

        return {
            "blockName": "uagb/container",
            "attrs": {
                "block_id": self._generate_block_id(),
                "contentPadding": {
                    "top": 40,
                    "bottom": 40,
                    "left": 20,
                    "right": 20
                }
            },
            "innerBlocks": [
                {
                    "blockName": "uagb/heading",
                    "attrs": {
                        "headingTitle": data.get("title", ""),
                        "headingTag": "h2",
                        "headingAlign": "center",
                        "headingColor": color_scheme.get("primary", "#2563eb")
                    }
                },
                {
                    "blockName": "core/paragraph",
                    "attrs": {
                        "content": data.get("content", ""),
                        "align": "center"
                    }
                }
            ]
        }

    def _generate_block_id(self) -> str:
        """
        Générer un ID unique pour un bloc
        """

        import uuid
        return str(uuid.uuid4())[:8]

    def export_to_json(self, blocks_config: Dict) -> str:
        """
        Exporter la configuration en JSON
        """

        return json.dumps(blocks_config, indent=2, ensure_ascii=False)
