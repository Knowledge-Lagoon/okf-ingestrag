import json
from pathlib import Path

from app.okf.validator import OKFValidator


class CatalogGenerator:
    """
    Builds catalog/index.json from valid OKF Markdown documents.

    The knowledge directory is the source of truth.
    The generated catalog is a searchable artifact and should not be
    edited manually.
    """

    DEFAULT_KNOWLEDGE_PATH = "knowledge"
    DEFAULT_CATALOG_FILE = "catalog/index.json"

    # Raw connector exports are stored in these staging directories.
    # They are excluded because they do not contain OKF YAML frontmatter.
    EXCLUDED_DIRECTORIES = {
        "confluence",
        "git",
    }

    @staticmethod
    def should_skip(
        file_path: Path,
        knowledge_root: Path,
    ) -> bool:
        """
        Return True when the document is inside an excluded staging
        directory.
        """

        try:
            relative_path = file_path.relative_to(
                knowledge_root
            )
        except ValueError:
            return True

        parent_directories = relative_path.parts[:-1]

        return any(
            directory
            in CatalogGenerator.EXCLUDED_DIRECTORIES
            for directory in parent_directories
        )

    @staticmethod
    def generate(
        knowledge_path=DEFAULT_KNOWLEDGE_PATH,
        catalog_file=DEFAULT_CATALOG_FILE,
    ):
        """
        Scan valid OKF Markdown documents and generate catalog/index.json.

        Returns:
            list: Generated catalog entries.
        """

        knowledge_root = Path(knowledge_path)
        catalog_path = Path(catalog_file)

        catalog = []

        # Ensure the catalog directory exists.
        catalog_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # If the knowledge directory does not exist, create an empty catalog.
        if not knowledge_root.exists():

            catalog_path.write_text(
                "[]",
                encoding="utf-8",
            )

            return catalog

        markdown_files = sorted(
            knowledge_root.rglob("*.md")
        )

        for file_path in markdown_files:

            # Ignore raw connector staging files.
            if CatalogGenerator.should_skip(
                file_path,
                knowledge_root,
            ):
                continue

            validation_result = (
                OKFValidator.validate(
                    str(file_path)
                )
            )

            # Only valid OKF documents are added to the catalog.
            if (
                validation_result["status"]
                != "VALID"
            ):
                continue

            metadata = (
                OKFValidator.extract_metadata(
                    str(file_path)
                )
            )

            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            catalog_entry = {
                "title": metadata["title"],
                "type": metadata["type"],
                "description": metadata[
                    "description"
                ],
                "tags": metadata["tags"],
                "owner": metadata["owner"],
                "version": str(
                    metadata.get(
                        "version",
                        "1.0",
                    )
                ),
                "source": metadata.get(
                    "source",
                    "manual",
                ),
                "path": str(file_path),
                "content": content,
            }

            catalog.append(
                catalog_entry
            )

        # Stable ordering makes testing and troubleshooting easier.
        catalog.sort(
            key=lambda document: (
                document["title"].lower(),
                document["path"].lower(),
            )
        )

        with catalog_path.open(
            "w",
            encoding="utf-8",
        ) as output_file:

            json.dump(
                catalog,
                output_file,
                indent=4,
                ensure_ascii=False,
            )

        return catalog