import json


class KnowledgeAnalyzer:

    def __init__(
        self,
        catalog_file="catalog/index.json"
    ):

        with open(
            catalog_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.catalog = json.load(f)

    def total_documents(self):

        return len(self.catalog)

    def documents_by_type(self):

        result = {}

        for doc in self.catalog:

            doc_type = doc.get(
                "type",
                "unknown"
            )

            result[doc_type] = (
                result.get(doc_type, 0) + 1
            )

        return result

    def documents_by_source(self):

        result = {}

        for doc in self.catalog:

            path = doc.get(
                "path",
                ""
            )

            if "imported" in path:

                source = "confluence"

            elif "runbooks" in path:

                source = "manual"

            elif "services" in path:

                source = "manual"

            elif "kubernetes" in path:

                source = "manual"

            else:

                source = "unknown"

            result[source] = (
                result.get(source, 0) + 1
            )

        return result

    def duplicate_titles(self):

        seen = {}
        duplicates = []

        for doc in self.catalog:

            title = (
                doc["title"]
                .lower()
                .strip()
            )

            if title in seen:

                duplicates.append(
                    doc["title"]
                )

            else:

                seen[title] = True

        return duplicates