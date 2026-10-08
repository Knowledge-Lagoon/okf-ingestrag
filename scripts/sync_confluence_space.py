import os
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

from app.connectors.confluence_connector import (
    ConfluenceConnector
)

from app.connectors.confluence_importer import (
    ConfluenceImporter
)

from app.connectors.confluence_okf_converter import (
    ConfluenceOKFConverter
)

from app.catalog.generator import (
    CatalogGenerator
)

from app.governance.report import (
    KnowledgeReport
)


BASE_URL = "https://knowledge-lagoon.atlassian.net"

SPACE_KEY = os.getenv(
    "CONFLUENCE_SPACE_KEY"
)

USERNAME = os.getenv(
    "CONFLUENCE_USERNAME"
)

API_TOKEN = os.getenv(
    "CONFLUENCE_API_TOKEN"
)


def main():
    print("LOADING SCRIPT")
    if not SPACE_KEY:
        raise ValueError(
            "CONFLUENCE_SPACE_KEY not set"
        )
    print("STARTING SYNC SCRIPT")
    connector = ConfluenceConnector(
        base_url=BASE_URL,
        username=USERNAME,
        api_token=API_TOKEN
    )

    pages = connector.get_space_pages(
        SPACE_KEY
    )

    print(
        f"Found {len(pages)} pages\n"
    )

    imported_count = 0

    for page in pages:

        page_id = page["id"]

if __name__ == "__main__":
    main()
        