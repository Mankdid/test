"""
Blueprint Manager - Gestion des blueprints réutilisables
"""

import json
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BlueprintManager:
    """
    Gestionnaire de blueprints pour sauvegarder et réutiliser des templates
    """

    def __init__(self, blueprints_dir: str = "blueprints"):
        self.blueprints_dir = blueprints_dir
        os.makedirs(blueprints_dir, exist_ok=True)

    def save_blueprint(
        self,
        template_id: str,
        business_name: str,
        site_structure: Dict,
        pages_content: Dict,
        color_scheme: Dict,
        astra_config: Dict,
        spectra_blocks: Dict,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Sauvegarder un template comme blueprint
        """

        blueprint_id = f"blueprint-{template_id}"

        blueprint_data = {
            "id": blueprint_id,
            "name": business_name,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "template": {
                "site_structure": site_structure,
                "pages_content": pages_content,
                "color_scheme": color_scheme,
                "astra_config": astra_config,
                "spectra_blocks": spectra_blocks
            }
        }

        # Sauvegarder le blueprint
        blueprint_path = os.path.join(self.blueprints_dir, f"{blueprint_id}.json")

        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(blueprint_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Blueprint sauvegardé: {blueprint_id}")

        return blueprint_id

    def load_blueprint(self, blueprint_id: str) -> Optional[Dict]:
        """
        Charger un blueprint existant
        """

        blueprint_path = os.path.join(self.blueprints_dir, f"{blueprint_id}.json")

        if not os.path.exists(blueprint_path):
            logger.warning(f"Blueprint non trouvé: {blueprint_id}")
            return None

        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint_data = json.load(f)

        logger.info(f"Blueprint chargé: {blueprint_id}")

        return blueprint_data

    def list_blueprints(self) -> List[Dict]:
        """
        Lister tous les blueprints disponibles
        """

        blueprints = []

        for filename in os.listdir(self.blueprints_dir):
            if filename.endswith(".json"):
                blueprint_path = os.path.join(self.blueprints_dir, filename)

                with open(blueprint_path, "r", encoding="utf-8") as f:
                    blueprint_data = json.load(f)

                blueprints.append({
                    "id": blueprint_data.get("id"),
                    "name": blueprint_data.get("name"),
                    "created_at": blueprint_data.get("created_at"),
                    "metadata": blueprint_data.get("metadata", {})
                })

        return sorted(blueprints, key=lambda x: x.get("created_at", ""), reverse=True)

    def delete_blueprint(self, blueprint_id: str) -> bool:
        """
        Supprimer un blueprint
        """

        blueprint_path = os.path.join(self.blueprints_dir, f"{blueprint_id}.json")

        if not os.path.exists(blueprint_path):
            logger.warning(f"Blueprint non trouvé: {blueprint_id}")
            return False

        os.remove(blueprint_path)
        logger.info(f"Blueprint supprimé: {blueprint_id}")

        return True

    def duplicate_blueprint(
        self,
        blueprint_id: str,
        new_name: str,
        modifications: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Dupliquer un blueprint avec modifications optionnelles
        """

        # Charger le blueprint source
        blueprint = self.load_blueprint(blueprint_id)

        if not blueprint:
            return None

        # Créer un nouvel ID
        new_id = f"blueprint-{new_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Copier et modifier
        new_blueprint = blueprint.copy()
        new_blueprint["id"] = new_id
        new_blueprint["name"] = new_name
        new_blueprint["created_at"] = datetime.now().isoformat()

        # Appliquer les modifications si fournies
        if modifications:
            if "color_scheme" in modifications:
                new_blueprint["template"]["color_scheme"] = modifications["color_scheme"]

            if "business_name" in modifications:
                new_blueprint["name"] = modifications["business_name"]

        # Sauvegarder le nouveau blueprint
        blueprint_path = os.path.join(self.blueprints_dir, f"{new_id}.json")

        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(new_blueprint, f, indent=2, ensure_ascii=False)

        logger.info(f"Blueprint dupliqué: {blueprint_id} -> {new_id}")

        return new_id

    def export_blueprint(self, blueprint_id: str, export_path: str) -> bool:
        """
        Exporter un blueprint vers un fichier
        """

        blueprint = self.load_blueprint(blueprint_id)

        if not blueprint:
            return False

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)

        logger.info(f"Blueprint exporté vers: {export_path}")

        return True

    def import_blueprint(self, import_path: str) -> Optional[str]:
        """
        Importer un blueprint depuis un fichier
        """

        if not os.path.exists(import_path):
            logger.warning(f"Fichier non trouvé: {import_path}")
            return None

        with open(import_path, "r", encoding="utf-8") as f:
            blueprint_data = json.load(f)

        # Générer un nouvel ID
        blueprint_id = blueprint_data.get("id", f"blueprint-imported-{datetime.now().strftime('%Y%m%d%H%M%S')}")

        # Sauvegarder
        blueprint_path = os.path.join(self.blueprints_dir, f"{blueprint_id}.json")

        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(blueprint_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Blueprint importé: {blueprint_id}")

        return blueprint_id

    def search_blueprints(self, query: str) -> List[Dict]:
        """
        Rechercher des blueprints par nom ou metadata
        """

        all_blueprints = self.list_blueprints()

        query_lower = query.lower()

        filtered_blueprints = [
            bp for bp in all_blueprints
            if query_lower in bp.get("name", "").lower()
            or query_lower in str(bp.get("metadata", {})).lower()
        ]

        return filtered_blueprints

    def get_blueprint_stats(self) -> Dict:
        """
        Obtenir des statistiques sur les blueprints
        """

        blueprints = self.list_blueprints()

        return {
            "total_blueprints": len(blueprints),
            "recent_blueprints": blueprints[:5],
            "storage_path": os.path.abspath(self.blueprints_dir)
        }
