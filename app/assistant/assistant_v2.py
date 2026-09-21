class AssistantV2:

    @staticmethod
    def build_response(context):

        response = []

        service = context.get(
            "service",
            {}
        )

        primary_document = (
            context.get(
                "primary_document",
                "Unknown"
            )
        )

        response.append(
            "\nKnowledge Assistant Response"
        )

        response.append(
            "=" * 50
        )

        response.append(
            f"\nPrimary Knowledge"
        )

        response.append(
            f"- {primary_document}"
        )

        #
        # Service Section
        #
        if service:

            response.append(
                "\nService Overview"
            )

            response.append(
                "-" * 30
            )

            runbooks = service.get(
                "runbooks",
                []
            )

            documentation = (
                service.get(
                    "documentation",
                    []
                )
            )

            owners = service.get(
                "owners",
                []
            )

            sources = service.get(
                "sources",
                []
            )

            tags = service.get(
                "tags",
                []
            )

            response.append(
                "\nRunbooks"
            )

            if runbooks:

                for item in runbooks:

                    response.append(
                        f"  - {item}"
                    )

            else:

                response.append(
                    "  None"
                )

            response.append(
                "\nDocumentation"
            )

            if documentation:

                for item in documentation:

                    response.append(
                        f"  - {item}"
                    )

            else:

                response.append(
                    "  None"
                )

            response.append(
                "\nOwners"
            )

            if owners:

                for owner in owners:

                    response.append(
                        f"  - {owner}"
                    )

            else:

                response.append(
                    "  None"
                )

            response.append(
                "\nSources"
            )

            if sources:

                for source in sources:

                    response.append(
                        f"  - {source}"
                    )

            else:

                response.append(
                    "  None"
                )

            response.append(
                "\nTags"
            )

            if tags:

                for tag in tags:

                    response.append(
                        f"  - {tag}"
                    )

            else:

                response.append(
                    "  None"
                )

        #
        # Relationship Section
        #
        related_documents = (
            context.get(
                "related_documents",
                []
            )
        )

        response.append(
            "\nRelated Knowledge"
        )

        response.append(
            "-" * 30
        )

        if related_documents:

            for item in related_documents:

                document = (
                    item.get(
                        "document",
                        "Unknown"
                    )
                )

                score = item.get(
                    "score",
                    0
                )

                tags = item.get(
                    "common_tags",
                    []
                )

                response.append(
                    f"- {document}"
                )

                response.append(
                    f"  Score: {score}"
                )

                response.append(
                    f"  Tags: "
                    f"{', '.join(tags)}"
                )

        else:

            response.append(
                "No related knowledge found"
            )

        response.append(
            "\nContext Package Complete"
        )

        return "\n".join(response)