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

from app.governance.report import (
    KnowledgeReport
)


if __name__ == "__main__":

    KnowledgeReport.generate()