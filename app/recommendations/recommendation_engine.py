import json


class RecommendationEngine:

    def __init__(
        self,
        graph_file="catalog/relationship_graph.json"
    ):

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.graph = json.load(f)

    def recommend(
        self,
        document_title,
        limit=5
    ):

        if (
            document_title
            not in self.graph
        ):

            return []

        recommendations = (
            self.graph[
                document_title
            ].get(
                "related",
                []
            )
        )

        recommendations = sorted(
            recommendations,
            key=lambda item:
                item.get(
                    "score",
                    0
                ),
            reverse=True
        )

        return recommendations[
            :limit
        ]