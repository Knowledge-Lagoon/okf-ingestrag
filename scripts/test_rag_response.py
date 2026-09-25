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

from app.rag.rag_response import (
    RAGResponse
)

package = EvidencePackage(

    question=
        "Why are pods restarting?",

    keyword_results=[
        {
            "title":
                "CrashLoopBackOff",

            "source":
                "confluence",

            "path":
                "knowledge/imported/crashloopbackoff.md"
        }
    ],

    graph_results=[
        {
            "document":
                "ImagePullBackOff"
        }
    ]
)

print(
    RAGResponse.build(
        package
    )
)