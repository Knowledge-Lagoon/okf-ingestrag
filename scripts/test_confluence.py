print("STARTING TEST SCRIPT")

import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

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


BASE_URL = "https://knowledge-lagoon.atlassian.net"

USERNAME = os.getenv(
    "CONFLUENCE_USERNAME"
)

API_TOKEN = os.getenv(
    "CONFLUENCE_API_TOKEN"
)

PAGE_ID = os.getenv(
    "CONFLUENCE_PAGE_ID"
)


def main():

    connector = ConfluenceConnector(
        base_url=BASE_URL,
        username=USERNAME,
        api_token=API_TOKEN
    )

    print("Connecting to Confluence...")

    page = connector.get_page_content(
        PAGE_ID
    )

    print("\nPage Retrieved Successfully\n")

    print(f"ID: {page['id']}")
    print(f"Title: {page['title']}")

    print("\nPage Keys:")
    print(page.keys())

    if "content" in page:
        print(
            f"\nContent Length: "
            f"{len(page['content'])}"
        )

    print("\nSaving page...\n")

    file_path = ConfluenceImporter.save_page(
        page
    )

    print(
        f"\nSaved to: {file_path}"
    )

    print(
        f"File Exists: "
        f"{Path(file_path).exists()}"
    )

    print("\nDone")


if __name__ == "__main__":
    main()