import json
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

from app.graph.relationship_graph import (
    RelationshipGraph
)


def main():

    graph = (
        RelationshipGraph()
        .build()
    )

    output_file = (
        Path(
            "catalog"
        )
        / "relationship_graph.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            graph,
            f,
            indent=4
        )

    print(
        f"Graph created: "
        f"{output_file}"
    )

    print(
        f"Nodes: "
        f"{len(graph)}"
    )


if __name__ == "__main__":
    main()