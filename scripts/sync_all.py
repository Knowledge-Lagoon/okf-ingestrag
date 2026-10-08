import sys
from pathlib import Path

project_root = (
    Path(__file__).resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(project_root)
)

from app.catalog.generator import (
    CatalogGenerator
)

from app.governance.report import (
    KnowledgeReport
)

from app.catalog.service_catalog import (
    ServiceCatalog
)


def main():

    print("\nSYNC ALL")
    print("=" * 50)

    #
    # Refresh catalog
    #
    print(
        "\nRefreshing catalog..."
    )

    catalog = (
        CatalogGenerator.generate()
    )

    print(
        f"Catalog entries: "
        f"{len(catalog)}"
    )

    #
    # Governance Report
    #
    print(
        "\nGenerating governance report..."
    )

    KnowledgeReport.generate()

    #
    # Service Report
    #
    print(
        "\nGenerating service catalog..."
    )

    catalog_service = (
        ServiceCatalog()
    )

    services = (
        catalog_service.build()
    )

    print(
        f"\nServices Found: "
        f"{len(services)}"
    )

    for service in services:

        print(
            f"- {service}"
        )

    print(
        "\nSync Complete"
    )


if __name__ == "__main__":
    main()