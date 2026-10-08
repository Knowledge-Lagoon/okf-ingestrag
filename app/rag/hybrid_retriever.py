from app.rag.evidence_package import (
    EvidencePackage
)

from app.search.engine import (
    SearchEngine
)

from app.graph.relationship_graph import (
    RelationshipGraph
)


class HybridRetriever:

    def __init__(self):

        self.search_engine = (
            SearchEngine()
        )

        self.graph = (
            RelationshipGraph()
            .build()
        )

    def retrieve(
        self,
        question
    ):

        #
        # Keyword Search
        #
        keyword_results = (
            self.search_engine.search(
                question
            )
        )

        #
        # Vector Search
        #
        # Disabled in v1.1.0
        #
        vector_results = []

        #
        # Graph Expansion
        #
        graph_results = []

        if keyword_results:

            primary = (
                keyword_results[0]
            )

            title = primary.get(
                "title"
            )

            if (
                title
                and
                title in self.graph
            ):

                graph_results = (
                    self.graph[
                        title
                    ].get(
                        "related",
                        []
                    )
                )

        return EvidencePackage(

            question=
                question,

            keyword_results=
                keyword_results,

            vector_results=
                vector_results,

            graph_results=
                graph_results,

            recommendations=
                graph_results
        )