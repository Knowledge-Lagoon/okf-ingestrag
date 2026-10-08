from pathlib import Path


class GitImporter:

    @staticmethod
    def import_document(
        source_file,
        output_dir="knowledge/git"
    ):

        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

        source_path = Path(source_file)

        destination = (
            Path(output_dir)
            / source_path.name
        )

        destination.write_text(
            source_path.read_text(
                encoding="utf-8",
                errors="ignore"
            ),
            encoding="utf-8"
        )

        return str(destination)