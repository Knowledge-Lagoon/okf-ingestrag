from app.catalog.generator import (
    CatalogGenerator
)

from app.governance.report import (
    KnowledgeReport
)

from app.catalog.service_catalog import (
    ServiceCatalog
)

from app.graph.relationship_graph import (
    RelationshipGraph
)


class PlatformService:

    def sync(self):

        print(
            "\nPlatform Sync"
        )

        print(
            "=" * 50
        )

        #
        # Catalog
        #
        catalog = (
            CatalogGenerator.generate()
        )

        print(
            f"\nCatalog Entries: "
            f"{len(catalog)}"
        )

        #
        # Governance
        #
        print(
            "\nGenerating Governance Report..."
        )

        KnowledgeReport.generate()

        #
        # Service Catalog
        #
        services = (
            ServiceCatalog()
            .build()
        )

        print(
            f"\nServices: "
            f"{len(services)}"
        )

        #
        # Relationship Graph
        #
        graph = (
            RelationshipGraph()
            .build()
        )

        print(
            f"Graph Nodes: "
            f"{len(graph)}"
        )

        print(
            "\nPlatform Sync Complete"
        )

        return {
            "catalog":
                len(catalog),
            "services":
                len(services),
            "graph":
                len(graph)
        }