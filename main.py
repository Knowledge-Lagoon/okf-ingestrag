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

    # Step 1
    scan_documents()

    # Step 2
    catalog = CatalogGenerator.generate()

    print(
        f"Catalog generated with {len(catalog)} entries\n"
    )

    # Step 3
    question = input("\nAsk a question: ").strip()

    if not question:
        print("Question cannot be empty")
        exit()

    print(f"\nQuestion: {question}")

    # Step 4
    keywords = KeywordExtractor.extract(question)

    keyword = KeywordExtractor.primary_keyword(question)

    print(f"Keywords: {keywords}")
    print(f"Primary Keyword: {keyword}")

    # Step 5
    route = QueryRouter.route(question)

    print(f"Route: {route}")

    # Step 6
    print("DEBUG: Starting search...")

    results = search(
        keyword,
        route
    )

    print("DEBUG: Search completed")
    print(f"DEBUG: Found {len(results)} results")

    if not results:
        print("\nNo matching documents found.")
        exit()

    print("DEBUG: Printing search results")

    print("\nSearch Results\n")

    for item in results:

        print(
            f"{item['title']} "
            f"(score={item['score']})"
        )

    # Step 7
    print("DEBUG: Building document context")

    top_docs = results[:1]

    combined_content = ""

    for doc in top_docs:

        print(
            f"DEBUG: Reading {doc['path']}"
        )

        content = DocumentRetriever.get_content(
            doc["path"]
        )

        combined_content += content

    print("DEBUG: Context built")

    # Step 8
    print("DEBUG: Building prompt")

    prompt = PromptBuilder.build(
        question,
        combined_content
    )

    print("DEBUG: Prompt built")

    # Step 9
    print("DEBUG: Initializing Ollama")

    ollama_service = OllamaService()

    print("DEBUG: Calling Ollama")

    response = ollama_service.ask(
        prompt
    )

    print("DEBUG: Ollama returned")

    # Step 10
    print("\nAI Response\n")

    print(response)

    # Step 11
    print("\nSource Documents\n")

    for doc in top_docs:

        print(
            f"- {doc['title']} "
            f"({doc['path']})"
        )