from pathlib import Path

from app.okf.validator import OKFValidator
from app.catalog.generator import CatalogGenerator
from app.router.router import QueryRouter
from app.search.service import search
from app.retrieval.retriever import DocumentRetriever
from app.assistant.knowledge_assistant import KnowledgeAssistant
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

    # Step 1: Validate documents
    scan_documents()

    # Step 2: Generate catalog
    catalog = CatalogGenerator.generate()

    print(f"Catalog generated with {len(catalog)} entries\n")

    # Step 3: Ask a question
    question = "How do I restart Kong?"

    print(f"Question: {question}\n")

    # Step 4: Route question
    route = QueryRouter.route(question)

    print(f"Route: {route}\n")

    # Step 5: Search
    results = search("kong", route)

    if not results:
        print("No matching documents found")
        exit()

    # Step 6: Show ranked results
    print("Search Results\n")

    for item in results:

        print(
            f"{item['title']} "
            f"(score={item['score']})"
        )

    # Step 7: Select best match
    doc = results[0]

    print("\nBest Match\n")

    print(doc["title"])

    # Step 8: Retrieve document
    content = DocumentRetriever.get_content(
        doc["path"]
    )

    # Step 9: Build assistant response
    content = DocumentRetriever.get_content(
        doc["path"]
    )
    prompt = PromptBuilder.build(
        question,
        content
    )
    ollama_service = OllamaService()
    response = ollama_service.ask(
        prompt
    )


    print("\nAI Response\n")

    print(response)

    print("\nDocument Source\n")

    print(doc["path"])