from pathlib import Path


class ConfluenceExporter:

    @staticmethod
    def export_page(
        title,
        content,
        output_dir="knowledge/confluence"
    ):

        Path(
            output_dir
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            title
            .lower()
            .replace(" ", "-")
        )

        output_file = (
            f"{output_dir}/{filename}.md"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return output_file