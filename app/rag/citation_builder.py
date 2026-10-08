class CitationBuilder:

    @staticmethod
    def build(
        evidence_package
    ):

        citations = []

        #
        # Keyword Matches
        #
        for item in (
            evidence_package
            .keyword_results
        ):

            citations.append({

                "title":
                    item.get(
                        "title"
                    ),

                "source":
                    item.get(
                        "source",
                        "unknown"
                    ),

                "path":
                    item.get(
                        "path",
                        "unknown"
                    )
            })

        #
        # Vector Matches
        #
        for item in (
            evidence_package
            .vector_results
        ):

            metadata = item.get(
                "metadata",
                {}
            )

            citations.append({

                "title":
                    metadata.get(
                        "title"
                    ),

                "source":
                    metadata.get(
                        "source"
                    ),

                "path":
                    metadata.get(
                        "path"
                    )
            })

        unique = []

        seen = set()

        for citation in citations:

            key = (
                citation[
                    "title"
                ]
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            unique.append(
                citation
            )

        return unique