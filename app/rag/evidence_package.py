class EvidencePackage:

    def __init__(
        self,
        question,
        keyword_results=None,
        vector_results=None,
        graph_results=None,
        recommendations=None
    ):

        self.question = question

        self.keyword_results = (
            keyword_results
            or []
        )

        self.vector_results = (
            vector_results
            or []
        )

        self.graph_results = (
            graph_results
            or []
        )

        self.recommendations = (
            recommendations
            or []
        )

    def to_dict(self):

        return {

            "question":
                self.question,

            "keyword_matches":
                self.keyword_results,

            "vector_matches":
                self.vector_results,

            "graph_matches":
                self.graph_results,

            "recommendations":
                self.recommendations
        }

    def source_count(self):

        sources = set()

        #
        # Keyword matches
        #
        for item in self.keyword_results:

            title = item.get(
                "title"
            )

            if title:

                sources.add(title)

        #
        # Vector matches
        #
        for item in self.vector_results:

            metadata = item.get(
                "metadata",
                {}
            )

            title = metadata.get(
                "title"
            )

            if title:

                sources.add(title)

        return len(
            sources
        )
