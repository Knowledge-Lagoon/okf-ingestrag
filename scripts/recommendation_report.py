print("STARTING RECOMMENDATION REPORT")

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

from app.recommendations.recommendation_engine import (
    RecommendationEngine
)


def main():

    document = "Kong Restart"

    print("\nCreating Recommendation Engine...")

    engine = RecommendationEngine()

    print(
        f"\nPrimary Document: "
        f"{document}"
    )

    print(
        "\nGetting recommendations..."
    )

    recommendations = (
        engine.recommend(
            document
        )
    )

    print(
        f"\nRecommendations Found: "
        f"{len(recommendations)}"
    )

    print(
        "\nRecommendations"
    )

    print(
        "=" * 50
    )

    if not recommendations:

        print(
            "\nNo recommendations found."
        )

        print(
            "\nPossible reasons:"
        )

        print(
            "- relationship_graph.json "
            "contains no relationships"
        )

        print(
            "- document title does "
            "not exist in graph"
        )

        return

    for item in recommendations:

        print(
            f"\nDocument: "
            f"{item.get('document')}"
        )

        print(
            f"Score: "
            f"{item.get('score', 0)}"
        )

        print(
            f"Shared Tags: "
            f"{', '.join(item.get('common_tags', []))}"
        )

    print(
        "\nRecommendation Report Complete"
    )


if __name__ == "__main__":
    main()