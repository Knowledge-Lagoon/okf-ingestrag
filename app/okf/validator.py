import yaml
from pathlib import Path


REQUIRED_FIELDS = [
    "type",
    "title",
    "description",
    "tags",
    "owner",
]


class OKFValidator:

    @staticmethod
    def extract_metadata(file_path: str):

        content = Path(file_path).read_text(encoding="utf-8")

        if not content.startswith("---"):
            raise ValueError("Missing YAML frontmatter")

        parts = content.split("---", 2)

        if len(parts) < 3:
            raise ValueError("Invalid frontmatter format")

        metadata = yaml.safe_load(parts[1])

        return metadata

    @staticmethod
    def validate(file_path: str):

        errors = []

        try:

            metadata = OKFValidator.extract_metadata(file_path)

            for field in REQUIRED_FIELDS:

                if field not in metadata:
                    errors.append(f"{field} missing")

            return {
                "status": "VALID" if not errors else "INVALID",
                "file": file_path,
                "errors": errors
            }

        except Exception as ex:

            return {
                "status": "INVALID",
                "file": file_path,
                "errors": [str(ex)]
            }