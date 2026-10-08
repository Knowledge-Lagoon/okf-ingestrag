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

from app.rag.evidence_package import (
    EvidencePackage
)

from app.rag.citation_builder import (
    CitationBuilder
)


package = EvidencePackage(

    question=
        "Why do pods restart?",

    keyword_results=[

        {
            "title":
                "CrashLoopBackOff",

            "source":
                "confluence",

            "path":
                "knowledge/imported/crashloopbackoff.md"
        }
    ]
)

print(
    "\nEvidence Package"
)

print(
    package.to_dict()
)

print(
    "\nCitations"
)

citations = (
    CitationBuilder
    .build(
        package
    )
)

for item in citations:

    print(
        item
    )