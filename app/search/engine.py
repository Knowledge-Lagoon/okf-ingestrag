import json


class SearchEngine:

    def __init__(self, catalog_file="catalog/index.json"):

        with open(catalog_file, "r") as f:
            self.catalog = json.load(f)

    def search(self, query: str):

        query = query.lower()

        results = []

        for doc in self.catalog:

            if query in doc["title"].lower():
                results.append(doc)
                continue

            if query in doc["type"].lower():
                results.append(doc)
                continue

            for tag in doc["tags"]:

                if query in tag.lower():
                    results.append(doc)
                    break

        return results