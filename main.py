from pathlib import Path

from app.okf.validator import OKFValidator
from app.catalog.generator import CatalogGenerator

from app.router.router import QueryRouter
from app.router.keyword_extractor import KeywordExtractor

from app.search.service import search
from app.retrieval.retriever import DocumentRetriever

from app.llm.ollama_service import OllamaService


MAX_CONTEXT_CHARACTERS = 1200
TOP_DOCUMENT_COUNT = 1


def scan_documents():

    files = list(
        Path("knowledge").rglob("*.md")
    )

    print(
        "\nScanning knowledge directory...\n"
    )

    valid_count = 0
    invalid_count = 0

    for file in files:

        result = OKFValidator.validate(
            str(file)
        )

        if result["status"] == "VALID":
            valid_count += 1
        else:
            invalid_count += 1

        print(result)

    print(
        f"\n{len(files)} documents found"
    )

    print(
        f"{valid_count} documents valid"
    )

    print(
        f"{invalid_count} staging or "
        "invalid documents excluded\n"
    )


def build_grounded_prompt(
    question,
    knowledge,
):

    return f"""
You are an enterprise DevOps knowledge assistant.

Answer only from the supplied knowledge.

If the supplied knowledge does not contain the answer,
state that the available knowledge is insufficient.

Keep the response concise.

Use these sections only when supported by the knowledge:

Summary
Recommended Action
Commands
Verification

Question:
{question}

Supplied knowledge:
{knowledge}
""".strip()


def main():

    # Step 1: Validate knowledge
    scan_documents()

    # Step 2: Generate catalog
    catalog = CatalogGenerator.generate()

    print(
        f"Catalog generated with "
        f"{len(catalog)} entries\n"
    )

    # Step 3: Read user question
    question = input(
        "\nAsk a question: "
    ).strip()

    if not question:

        print(
            "Question cannot be empty."
        )

        return

    print(
        f"\nQuestion: {question}"
    )

    # Step 4: Extract keywords
    keywords = KeywordExtractor.extract(
        question
    )

    keyword = (
        KeywordExtractor.primary_keyword(
            question
        )
    )

    print(
        f"Keywords: {keywords}"
    )

    print(
        f"Primary Keyword: {keyword}"
    )

    # Step 5: Route the query
    route = QueryRouter.route(
        question
    )

    print(
        f"Route: {route}"
    )

    # Step 6: Search catalog
    print(
        "\nSearching knowledge..."
    )

    results = search(
        keyword,
        route,
    )

    if not results:

        print(
            "\nNo matching knowledge found."
        )

        return

    print(
        f"Found {len(results)} result(s)."
    )

    print(
        "\nSearch Results"
    )

    print(
        "-" * 50
    )

    for item in results:

        print(
            f"- {item['title']} "
            f"(score={item['score']})"
        )

    # Step 7: Retrieve top document
    top_docs = results[
        :TOP_DOCUMENT_COUNT
    ]

    context_parts = []

    print(
        "\nRetrieving source content..."
    )

    for document in top_docs:

        path = document["path"]

        print(
            f"- Reading {path}"
        )

        content = (
            DocumentRetriever.get_content(
                path
            )
        )

        if not content:
            continue

        context_parts.append(
            content[
                :MAX_CONTEXT_CHARACTERS
            ]
        )

    combined_content = "\n\n".join(
        context_parts
    ).strip()

    if not combined_content:

        print(
            "\nNo readable content was retrieved."
        )

        return

    print(
        f"Retrieved context length: "
        f"{len(combined_content)} characters"
    )

    # Step 8: Display retrieved evidence
    print(
        "\nRetrieved Knowledge Preview"
    )

    print(
        "-" * 50
    )

    print(
        combined_content[:500]
    )

    print(
        "\nSource Documents"
    )

    print(
        "-" * 50
    )

    for document in top_docs:

        print(
            f"- {document['title']} "
            f"({document['path']})"
        )

    # Step 9: Build grounded prompt
    prompt = build_grounded_prompt(
        question=question,
        knowledge=combined_content,
    )

    print(
        f"\nGrounded prompt length: "
        f"{len(prompt)} characters"
    )

    # Step 10: Generate grounded response
    print(
        "\nGenerating grounded answer..."
    )

    ollama_service = OllamaService()

    response = ollama_service.ask(
        prompt
    )

    # Step 11: Present response
    print(
        "\nAI Response"
    )

    print(
        "=" * 50
    )

    print(response)

    print(
        "\nEvidence"
    )

    print(
        "=" * 50
    )

    for document in top_docs:

        print(
            f"- {document['title']}"
        )

        print(
            f"  Source: "
            f"{document.get('source', 'unknown')}"
        )

        print(
            f"  Path: {document['path']}"
        )


if __name__ == "__main__":
    main()