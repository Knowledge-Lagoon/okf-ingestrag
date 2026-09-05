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