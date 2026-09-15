import sys
from pathlib import Path

project_root = (
    Path(__file__).resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(project_root)
)

from app.connectors.git_connector import (
    GitConnector
)

from app.connectors.git_importer import (
    GitImporter
)

from app.connectors.git_okf_converter import (
    GitOKFConverter
)

REPO_PATH = "./sample_repo"


def main():

    connector = GitConnector(
        REPO_PATH
    )

    docs = (
        connector.discover_documents()
    )

    print(
        f"Found {len(docs)} files"
    )

    for doc in docs:

        imported = (
            GitImporter.import_document(
                doc
            )
        )

        okf_file = (
            GitOKFConverter.convert(
                imported
            )
        )

        print(
            f"Imported: {okf_file}"
        )


if __name__ == "__main__":
    main()