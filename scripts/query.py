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

from app.rag.hybrid_retriever import (
    HybridRetriever
)

from app.rag.rag_response import (
    RAGResponse
)


def main():

    print(
        "\nOKF-IngestRAG"
    )

    print(
        "=" * 60
    )

    print(
        "\nHybrid Knowledge Retrieval"
    )

    print(
        "Type 'exit' to quit."
    )

    retriever = (
        HybridRetriever()
    )

    while True:

        question = input(
            "\nAsk a question: "
        ).strip()

        if not question:
            continue

        if question.lower() in [
            "exit",
            "quit"
        ]:
            break

        try:

            evidence_package = (
                retriever.retrieve(
                    question
                )
            )

            response = (
                RAGResponse.build(
                    evidence_package
                )
            )

            print(
                "\n"
            )

            print(
                response
            )

        except Exception as ex:

            print(
                "\nError:"
            )

            print(
                str(ex)
            )

    print(
        "\nGoodbye."
    )


if __name__ == "__main__":
    main()