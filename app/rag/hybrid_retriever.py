from app.rag.evidence_package import (
    EvidencePackage
)

from app.rag.retriever import (
    SemanticRetriever
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

        self.semantic_retriever = (
            SemanticRetriever()
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
        try:

            vector_results = (
                self.semantic_retriever
                .retrieve(
                    question,
                    limit=5
                )
            )

        except Exception:

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

            if title:

                graph_results = (
                    self.graph.get(
                        title,
                        {}
                    ).get(
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
                graph_results
        )