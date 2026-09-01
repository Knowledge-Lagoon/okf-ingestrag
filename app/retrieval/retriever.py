from pathlib import Path


class DocumentRetriever:

    @staticmethod
    def get_content(path: str):

        return Path(path).read_text(
            encoding="utf-8"
        )