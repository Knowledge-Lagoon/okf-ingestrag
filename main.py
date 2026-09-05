from pathlib import Path

from app.okf.validator import OKFValidator
from app.catalog.generator import CatalogGenerator

from app.router.router import QueryRouter
from app.router.keyword_extractor import KeywordExtractor

from app.search.service import search

from app.retrieval.retriever import DocumentRetriever

from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_service import OllamaService


def scan_documents():

    files = list(Path("knowledge").rglob("*.md"))

    print("\nScanning knowledge directory...\n")

    valid_count = 0

    for file in files:

        result = OKFValidator.validate(str(file))

        if result["status"] == "VALID":
            valid_count += 1

        print(result)

    print(f"\n{len(files)} documents found")
    print(f"{valid_count} documents valid\n")


if __name__ == "__main__":

    # Step 1 - Validate knowledge documents
    scan_documents()

    # Step 2 - Generate catalog
    catalog = CatalogGenerator.generate()

    print(
        f"Catalog generated with {len(catalog)} entries\n"
    )

    # Step 3 - Ask user question
    question = input(
        "\nAsk a question: "
    ).strip()

    if not question:
        print("Question cannot be empty")
        exit()

    print(f"\nQuestion: {question}")

    # Step 4 - Extract keyword
    keyword = KeywordExtractor.primary_keyword(
        question
    )

    print(f"Keyword: {keyword}")

    # Step 5 - Route question
    route = QueryRouter.route(question)

    print(f"Route: {route}")

    # Step 6 - Search
    results = search(
        keyword,
        route
    )

    if not results:
        print(
            "\nNo matching documents found."
        )
        exit()

    print("\nSearch Results\n")

    for item in results:

        print(
            f"{item['title']} "
            f"(score={item['score']})"
        )

    # Step 7 - Select top 3 documents
    top_docs = results[:3]

    combined_content = ""

    print("\nDocuments Used\n")

    for doc in top_docs:

        print(
            f"- {doc['title']} "
            f"({doc['path']})"
        )

        combined_content += (
            f"\n\n=== {doc['title']} ===\n\n"
        )

        combined_content += (
            DocumentRetriever.get_content(
                doc["path"]
            )
        )

    # Step 8 - Build prompt
    prompt = PromptBuilder.build(
        question,
        combined_content
    )

    # Step 9 - Query Ollama
    ollama_service = OllamaService()

    response = ollama_service.ask(
        prompt
    )

    # Step 10 - Display AI response
    print("\nAI Response\n")

    print(response)

    # Step 11 - Show source documents
    print("\nSource Documents\n")

    for doc in top_docs:

        print(
            f"- {doc['title']} "
            f"({doc['path']})"
        )