from app.governance.analyzer import (
    KnowledgeAnalyzer
)


class KnowledgeReport:

    @staticmethod
    def generate():

        analyzer = KnowledgeAnalyzer()

        print("\nKnowledge Report")
        print("=" * 50)

        #
        # Summary
        #
        print(
            f"\nTotal Documents: "
            f"{analyzer.total_documents()}"
        )

        print(
            f"Knowledge Quality Score: "
            f"{analyzer.quality_score()}%"
        )

        #
        # Documents by Type
        #
        print("\nDocuments By Type")
        print("-" * 30)

        for (
            doc_type,
            count
        ) in (
            analyzer.documents_by_type()
            .items()
        ):

            print(
                f"- {doc_type}: {count}"
            )

        #
        # Documents by Source
        #
        print("\nDocuments By Source")
        print("-" * 30)

        for (
            source,
            count
        ) in (
            analyzer.documents_by_source()
            .items()
        ):

            print(
                f"- {source}: {count}"
            )

        #
        # Duplicate Detection
        #
        duplicates = (
            analyzer.duplicate_titles()
        )

        print("\nPotential Duplicates")
        print("-" * 30)

        if duplicates:

            for item in duplicates:

                print(
                    f"- {item}"
                )

        else:

            print("None")

        #
        # Missing Owners
        #
        print("\nMissing Owners")
        print("-" * 30)

        missing = (
            analyzer.missing_owners()
        )

        if missing:

            for doc in missing:

                print(
                    f"- {doc}"
                )

        else:

            print("None")

        #
        # Missing Tags
        #
        print("\nMissing Tags")
        print("-" * 30)

        missing = (
            analyzer.missing_tags()
        )

        if missing:

            for doc in missing:

                print(
                    f"- {doc}"
                )

        else:

            print("None")

        #
        # Missing Descriptions
        #
        print("\nMissing Descriptions")
        print("-" * 30)

        missing = (
            analyzer
            .missing_descriptions()
        )

        if missing:

            for doc in missing:

                print(
                    f"- {doc}"
                )

        else:

            print("None")

        print(
            "\nGovernance Report Complete\n"
        )