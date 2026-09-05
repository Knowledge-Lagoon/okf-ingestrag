from pathlib import Path


class ConfluenceImporter:

    @staticmethod
    def save_page(
        title,
        content,
        output_dir="knowledge/confluence"
    ):

        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            title.lower()
            .replace(" ", "-")
            .replace("/", "-")
        )

        file_path = (
            f"{output_dir}/{filename}.md"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return file_path