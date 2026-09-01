import json
from pathlib import Path

from app.okf.validator import OKFValidator


class CatalogGenerator:

    @staticmethod
    def generate(knowledge_path="knowledge"):

        catalog = []

        for file in Path(knowledge_path).rglob("*.md"):

            result = OKFValidator.validate(str(file))

            if result["status"] == "VALID":

                metadata = OKFValidator.extract_metadata(str(file))
                content = Path(file).read_text(encoding="utf-8")

                catalog.append(
                    {
                        "title": metadata["title"],
                        "type": metadata["type"],
                        "description": metadata["description"],
                        "tags": metadata["tags"],
                        "owner": metadata["owner"],
                        "path": str(file),
                        "content": content
                    }
                )

        Path("catalog").mkdir(exist_ok=True)

        with open("catalog/index.json", "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=4)

        return catalog