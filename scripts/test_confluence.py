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

    if not USERNAME:
        raise ValueError(
            "CONFLUENCE_USERNAME not set"
        )

    if not API_TOKEN:
        raise ValueError(
            "CONFLUENCE_API_TOKEN not set"
        )

    if not PAGE_ID:
        raise ValueError(
            "CONFLUENCE_PAGE_ID not set"
        )

    connector = ConfluenceConnector(
        base_url=BASE_URL,
        username=USERNAME,
        api_token=API_TOKEN
    )

    print(
        "Connecting to Confluence..."
    )

    page = connector.get_page(
        PAGE_ID
    )

    print(
        "\nPage Retrieved Successfully\n"
    )

    print(
        f"ID: {page['id']}"
    )

    print(
        f"Title: {page['title']}"
    )

    print(
        f"Type: {page['type']}"
    )


if __name__ == "__main__":
    main()