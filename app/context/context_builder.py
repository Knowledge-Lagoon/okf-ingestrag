import json

from app.catalog.service_catalog import (
    ServiceCatalog
)


class ContextBuilder:

    def __init__(
        self,
        graph_file="catalog/relationship_graph.json"
    ):

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.graph = json.load(f)

        self.service_catalog = (
            ServiceCatalog()
        )

        self.services = (
            self.service_catalog.build()
        )

    def build(
        self,
        query,
        document
    ):

        title = document.get(
            "title",
            ""
        )

        service_name = (
            title.split()[0]
            if title
            else ""
        )

        related = (
            self.graph.get(
                title,
                {}
            )
            .get(
                "related",
                []
            )
        )

        service_info = (
            self.services.get(
                service_name,
                {}
            )
        )

        return {
            "query": query,
            "primary_document": title,
            "document_type": document.get(
                "type"
            ),
            "source": document.get(
                "source"
            ),
            "related_documents": related,
            "service": service_info
        }