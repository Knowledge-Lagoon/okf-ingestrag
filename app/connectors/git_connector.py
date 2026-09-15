from pathlib import Path


class GitConnector:

    def __init__(self, repo_path):

        self.repo_path = Path(repo_path)

    def discover_documents(self):

        documents = []

        for ext in [
            "*.md",
            "*.txt"
        ]:

            for file in self.repo_path.rglob(ext):

                documents.append(file)

        return documents