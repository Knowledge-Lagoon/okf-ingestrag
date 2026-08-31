from dataclasses import dataclass
from typing import List


@dataclass
class OKFDocument:
    title: str
    doc_type: str
    description: str
    tags: List[str]
    owner: str
    version: str
    path: str
