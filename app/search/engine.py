import json


class SearchEngine:

    def __init__(self, catalog_file="catalog/index.json"):

        with open(catalog_file, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def search(self, query: str, doc_type=None):

        query = query.lower()

        results = []

        for doc in self.catalog:

            # Filter by document type if provided
            if doc_type and doc["type"] != doc_type:
                continue

            # Search title
            if query in doc["title"].lower():
                results.append(doc)
                continue

            # Search type
            if query in doc["type"].lower():
                results.append(doc)
                continue

            # Search description
            if query in doc.get("description", "").lower():
                results.append(doc)
                continue

            # Search tags
            for tag in doc.get("tags", []):

                if query in tag.lower():
                    results.append(doc)
                    break

            # Search content
            if query in doc.get("content", "").lower():

                # Avoid duplicates
                if doc not in results:
                    results.append(doc)

        return results