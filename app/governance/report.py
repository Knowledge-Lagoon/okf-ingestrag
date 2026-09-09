from app.governance.analyzer import (
    KnowledgeAnalyzer
)


class KnowledgeReport:

    @staticmethod
    def generate():

        analyzer = KnowledgeAnalyzer()

        print("\nKnowledge Report")
        print("====================")

        print(
            f"\nTotal Documents: "
            f"{analyzer.total_documents()}"
        )

        print("\nDocuments By Type")

        for (
            doc_type,
            count
        ) in analyzer.documents_by_type().items():

            print(
                f"- {doc_type}: {count}"
            )

        print("\nDocuments By Source")

        for (
            source,
            count
        ) in analyzer.documents_by_source().items():

            print(
                f"- {source}: {count}"
            )

        duplicates = (
            analyzer.duplicate_titles()
        )

        print("\nPotential Duplicates")

        if duplicates:

            for item in duplicates:

                print(
                    f"- {item}"
                )

        else:

            print("None")