from pathlib import Path

from app.okf.validator import OKFValidator
from app.catalog.generator import CatalogGenerator
from app.search.service import search

from app.router.router import QueryRouter
from app.search.service import search


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

    # Uncomment or add functionality here
    # scan_documents()

    # catalog = CatalogGenerator.generate()

    # print(f"Catalog generated with {len(catalog)} entries")
    # print("\nSearch Results\n")

    # #results = search("kubernetes")
    # results = search("grafana")

    # for item in results:

    #     print(item["title"])
    

    question = "How do I restart Kong?"

    route = QueryRouter.route(question)

    print(f"Route: {route}")

    results = search("kong", route)

    for item in results:
        print(item["title"])