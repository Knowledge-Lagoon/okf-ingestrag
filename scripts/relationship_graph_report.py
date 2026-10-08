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
    ).build()

    print(
        "\nRelationship Graph"
    )

    print(
        "=" * 50
    )

    for (
        document,
        data
    ) in graph.items():

        print(
            f"\n{document}"
        )

        print(
            "-" * 40
        )

        if not data[
            "related"
        ]:

            print(
                "No relationships"
            )

            continue

        for item in data[
            "related"
        ]:

            print(
                f"- {item['document']}"
                f" "
                f"{item['common_tags']}"
            )


if __name__ == "__main__":
    main()