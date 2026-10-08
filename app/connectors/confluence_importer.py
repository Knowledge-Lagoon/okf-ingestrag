from pathlib import Path


class ConfluenceImporter:

    @staticmethod
    def save_page(page):

        output_dir = "knowledge/confluence"

        print("DEBUG: Creating output directory")

        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            page["title"]
            .lower()
            .replace(" ", "-")
            .replace("/", "-")
        )

        file_path = (
            f"{output_dir}/{filename}.md"
        )

        print(f"DEBUG: Writing file: {file_path}")

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(page["content"])

        print("DEBUG: File write completed")

        return file_path