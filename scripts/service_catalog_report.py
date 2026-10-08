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

from app.catalog.service_catalog import (
    ServiceCatalog
)


def main():

    catalog = ServiceCatalog()

    services = catalog.build()

    print("\nService Catalog Report")
    print("========================")

    if not services:

        print("\nNo services found.")
        return

    for (
        service,
        documents
    ) in services.items():

        print(f"\nService: {service}")

        print("-" * 40)

        for document in documents:

            print(
                f"  - {document}"
            )

    print(
        f"\nTotal Services: "
        f"{len(services)}"
    )


if __name__ == "__main__":
    main()