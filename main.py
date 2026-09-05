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

    # Validate documents
    scan_documents()

    # Generate catalog
    catalog = CatalogGenerator.generate()
    print(
        f"Catalog generated with {len(catalog)} entries\n"
    )

    # User question
    question = input(
        "\nAsk a question: "
    ).strip()

    if not question:
        print("Question cannot be empty")
        exit()

    print(f"\nQuestion: {question}")
    # Extract keywords
    keywords = KeywordExtractor.extract(
        question
    )

    keyword = KeywordExtractor.primary_keyword(
        question
    )

    print(f"Keywords: {keywords}")
    print(f"Primary Keyword: {keyword}")

    # Route query
    route = QueryRouter.route(question)

    print(f"Route: {route}")
    print("DEBUG: Starting search...")

    # Search
    results = search(
        keyword
    )
    results = search(
        keyword,
        route
    )

    print("DEBUG: Search completed")
    print(f"DEBUG: Found {len(results)} results")