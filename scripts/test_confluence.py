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
    "CONFLUENCE_PAGE"
)

page = connector.get_page_content(PAGE_ID)

print("\nPage Retrieved Successfully\n")

print(f"ID: {page['id']}")
print(f"Title: {page['title']}")

from app.connectors.confluence_importer import (
    ConfluenceImporter
)

file_path = ConfluenceImporter.save_page(page)

print(f"\nSaved to: {file_path}")

print("\nFile exists?")

from pathlib import Path

print(Path(file_path).exists())