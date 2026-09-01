from pathlib import Path

from app.okf.validator import OKFValidator
from app.catalog.generator import CatalogGenerator
from app.search.service import search
from app.router.router import QueryRouter
from app.retrieval.retriever import DocumentRetriever


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

    # Step 1: Validate documents
    scan_documents()

    # Step 2: Generate catalog
    catalog = CatalogGenerator.generate()

    print(f"Catalog generated with {len(catalog)} entries\n")

    # Step 3: User question
    question = "How do I restart Kong?"

    # Step 4: Route query
    route = QueryRouter.route(question)

    print(f"Route: {route}")

    # Step 5: Search
    results = search("kong", route)

    if not results:
        print("No documents found")
        exit()

    # Step 6: Display results
    print("\nSearch Results\n")

    for item in results:
        print(item["title"])

    # Step 7: Retrieve first matching document
    doc = results[0]

    print("\nDocument Selected:\n")
    print(doc["title"])

    print("\nDocument Content:\n")

    print(
        DocumentRetriever.get_content(
            doc["path"]
        )
    )        