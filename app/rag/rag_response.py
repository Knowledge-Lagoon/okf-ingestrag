from app.rag.citation_builder import (
    CitationBuilder
)


class RAGResponse:

    @staticmethod
    def build(
        evidence_package
    ):

        response = []

        response.append(
            "\nRAG Response"
        )

        response.append(
            "=" * 60
        )

        response.append(
            f"\nQuestion:\n"
            f"{evidence_package.question}"
        )

        #
        # Sources
        #
        citations = (
            CitationBuilder
            .build(
                evidence_package
            )
        )

        response.append(
            "\nSources"
        )

        response.append(
            "-" * 30
        )

        if citations:

            for item in citations:

                response.append(
                    f"Title : {item['title']}"
                )

                response.append(
                    f"Source: {item['source']}"
                )

                response.append(
                    f"Path  : {item['path']}"
                )

                response.append("")
        else:

            response.append(
                "No sources available"
            )

        #
        # Related Knowledge
        #
        response.append(
            "\nRelated Knowledge"
        )

        response.append(
            "-" * 30
        )

        if (
            evidence_package.graph_results
        ):

            for item in (
                evidence_package
                .graph_results
            ):

                response.append(
                    f"- {item.get('document')}"
                )

        else:

            response.append(
                "No related knowledge"
            )

        #
        # Traceability
        #
        response.append(
            "\nRetrieval Trace"
        )

        response.append(
            "-" * 30
        )

        response.append(
            f"Keyword Matches: "
            f"{len(evidence_package.keyword_results)}"
        )

        response.append(
            f"Vector Matches: "
            f"{len(evidence_package.vector_results)}"
        )

        response.append(
            f"Graph Matches: "
            f"{len(evidence_package.graph_results)}"
        )

        response.append(
            f"Unique Sources: "
            f"{evidence_package.source_count()}"
        )

        return "\n".join(response)