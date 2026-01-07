"""
WordPress WXR Generator - Génération de fichiers WordPress eXtended RSS
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class WordPressGenerator:
    """
    Générateur de fichiers WXR (WordPress eXtended RSS) pour l'import WordPress
    """

    def __init__(self):
        self.wp_version = "6.4"
        self.base_url = "https://example.com"

    def generate_wxr(
        self,
        business_name: str,
        site_structure: Dict,
        pages_content: Dict[str, Dict],
        language: str = "fr-FR"
    ) -> str:
        """
        Générer un fichier WXR complet
        """

        # Créer la structure XML de base
        rss = ET.Element("rss", {
            "version": "2.0",
            "xmlns:excerpt": "http://wordpress.org/export/1.2/excerpt/",
            "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
            "xmlns:wfw": "http://wellformedweb.org/CommentAPI/",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
            "xmlns:wp": "http://wordpress.org/export/1.2/"
        })

        channel = ET.SubElement(rss, "channel")

        # Informations du site
        ET.SubElement(channel, "title").text = business_name
        ET.SubElement(channel, "link").text = self.base_url
        ET.SubElement(channel, "description").text = f"Site généré automatiquement pour {business_name}"
        ET.SubElement(channel, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        ET.SubElement(channel, "language").text = language
        ET.SubElement(channel, "wp:wxr_version").text = "1.2"
        ET.SubElement(channel, "wp:base_site_url").text = self.base_url
        ET.SubElement(channel, "wp:base_blog_url").text = self.base_url

        # Auteur par défaut
        author = ET.SubElement(channel, "wp:author")
        ET.SubElement(author, "wp:author_id").text = "1"
        ET.SubElement(author, "wp:author_login").text = "admin"
        ET.SubElement(author, "wp:author_email").text = "admin@example.com"
        ET.SubElement(author, "wp:author_display_name").text = "Admin"
        ET.SubElement(author, "wp:author_first_name").text = "Admin"
        ET.SubElement(author, "wp:author_last_name").text = ""

        # Générer les pages
        post_id = 1
        for page in site_structure.get("pages", []):
            page_slug = page.get("slug", "page")
            page_content = pages_content.get(page_slug, {})

            post_id = self._add_page(
                channel=channel,
                post_id=post_id,
                page_slug=page_slug,
                page_data=page,
                page_content=page_content
            )
            post_id += 1

        # Générer le menu de navigation
        self._add_navigation_menu(channel, site_structure.get("navigation", []), post_id)

        # Convertir en string XML formaté
        xml_string = self._prettify_xml(rss)

        logger.info(f"Fichier WXR généré avec {len(site_structure.get('pages', []))} pages")

        return xml_string

    def _add_page(
        self,
        channel: ET.Element,
        post_id: int,
        page_slug: str,
        page_data: Dict,
        page_content: Dict
    ) -> int:
        """
        Ajouter une page au fichier WXR
        """

        item = ET.SubElement(channel, "item")

        page_title = page_content.get("page_title", page_data.get("name", "Page"))

        # Informations de base
        ET.SubElement(item, "title").text = page_title
        ET.SubElement(item, "link").text = f"{self.base_url}/{page_slug}/"
        ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        ET.SubElement(item, "dc:creator").text = "admin"
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = f"{self.base_url}/?page_id={post_id}"
        ET.SubElement(item, "description")

        # Contenu de la page en blocs Gutenberg
        content = self._generate_gutenberg_content(page_content)
        ET.SubElement(item, "content:encoded").text = f"<![CDATA[{content}]]>"

        ET.SubElement(item, "excerpt:encoded").text = f"<![CDATA[{page_content.get('meta_description', '')}]]>"

        # Meta WordPress
        ET.SubElement(item, "wp:post_id").text = str(post_id)
        ET.SubElement(item, "wp:post_date").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:post_date_gmt").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:post_modified").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:post_modified_gmt").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:comment_status").text = "closed"
        ET.SubElement(item, "wp:ping_status").text = "closed"
        ET.SubElement(item, "wp:post_name").text = page_slug
        ET.SubElement(item, "wp:status").text = "publish"
        ET.SubElement(item, "wp:post_parent").text = "0"
        ET.SubElement(item, "wp:menu_order").text = "0"
        ET.SubElement(item, "wp:post_type").text = "page"
        ET.SubElement(item, "wp:post_password")
        ET.SubElement(item, "wp:is_sticky").text = "0"

        return post_id

    def _generate_gutenberg_content(self, page_content: Dict) -> str:
        """
        Générer le contenu en blocs Gutenberg
        """

        sections = page_content.get("sections", {})
        gutenberg_blocks = []

        for section_name, section_data in sections.items():
            if section_name == "hero":
                gutenberg_blocks.append(self._create_hero_block(section_data))
            elif "items" in section_data:
                gutenberg_blocks.append(self._create_columns_block(section_data))
            else:
                gutenberg_blocks.append(self._create_section_block(section_data))

        return "\n\n".join(gutenberg_blocks)

    def _create_hero_block(self, data: Dict) -> str:
        """
        Créer un bloc hero avec Cover block
        """

        title = data.get("title", "")
        subtitle = data.get("subtitle", "")
        cta_text = data.get("cta_text", "")

        return f'''<!-- wp:cover {{"dimRatio":50,"overlayColor":"primary","align":"full"}} -->
<div class="wp-block-cover alignfull"><span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span><div class="wp-block-cover__inner-container">
<!-- wp:heading {{"textAlign":"center","level":1,"fontSize":"huge"}} -->
<h1 class="has-text-align-center has-huge-font-size">{title}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {{"align":"center","fontSize":"large"}} -->
<p class="has-text-align-center has-large-font-size">{subtitle}</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"center"}}}} -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="#contact">{cta_text}</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->
</div></div>
<!-- /wp:cover -->'''

    def _create_columns_block(self, data: Dict) -> str:
        """
        Créer un bloc avec colonnes pour les items
        """

        title = data.get("title", "")
        items = data.get("items", [])

        blocks = [f'''<!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="has-text-align-center">{title}</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns">''']

        for item in items[:3]:  # Max 3 colonnes
            item_title = item.get("title", "")
            item_desc = item.get("description", "")

            blocks.append(f'''<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":3}} -->
<h3>{item_title}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{item_desc}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->''')

        blocks.append("</div>\n<!-- /wp:columns -->")

        return "\n".join(blocks)

    def _create_section_block(self, data: Dict) -> str:
        """
        Créer un bloc de section simple
        """

        title = data.get("title", "")
        content = data.get("content", "")

        return f'''<!-- wp:group {{"layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group"><!-- wp:heading {{"textAlign":"center"}} -->
<h2 class="has-text-align-center">{title}</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{content}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->'''

    def _add_navigation_menu(self, channel: ET.Element, navigation: List[str], start_id: int):
        """
        Ajouter le menu de navigation
        """

        # Créer le terme de menu
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = "Menu Principal"
        ET.SubElement(item, "wp:post_id").text = str(start_id)
        ET.SubElement(item, "wp:post_type").text = "nav_menu_item"
        ET.SubElement(item, "wp:status").text = "publish"

    def _prettify_xml(self, elem: ET.Element) -> str:
        """
        Formatter le XML de manière lisible
        """

        rough_string = ET.tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)

        return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
