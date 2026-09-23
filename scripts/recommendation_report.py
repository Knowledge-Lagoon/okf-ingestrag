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

    document = (
        "Kong Restart"
    )

    engine = (
        RecommendationEngine()
    )

    recommendations = (
        engine.recommend(
            document
        )
    )

    print(
        "\nRecommendations"
    )

    print(
        "=" * 50
    )

    print(
        f"\nPrimary Document:"
    )

    print(
        f"{document}"
    )

    print(
        "\nRecommended Knowledge"
    )

    print(
        "-" * 30
    )

    if not recommendations:

        print(
            "No recommendations found"
        )

        return

    for item in recommendations:

        print(
            f"- {item['document']}"
        )

        print(
            f"  Score: "
            f"{item['score']}"
        )

        print(
            f"  Tags: "
            f"{', '.join(item['common_tags'])}"
        )