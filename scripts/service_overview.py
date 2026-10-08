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

    print("\nService Overview")
    print("============================")

    if not services:

        print("\nNo services found.")
        return

    for (
        service_name,
        service
    ) in services.items():

        print(
            f"\nService: {service_name}"
        )

        print(
            "-" * 50
        )

        print("\nRunbooks")

        if service["runbooks"]:

            for item in service[
                "runbooks"
            ]:

                print(
                    f"  - {item}"
                )

        else:

            print(
                "  None"
            )

        print(
            "\nDocumentation"
        )

        if service[
            "documentation"
        ]:

            for item in service[
                "documentation"
            ]:

                print(
                    f"  - {item}"
                )

        else:

            print(
                "  None"
            )

        print("\nOwners")

        for owner in service[
            "owners"
        ]:

            print(
                f"  - {owner}"
            )

        print("\nSources")

        for source in service[
            "sources"
        ]:

            print(
                f"  - {source}"
            )

        print("\nTags")

        for tag in service[
            "tags"
        ]:

            print(
                f"  - {tag}"
            )

    print(
        f"\nTotal Services: "
        f"{len(services)}"
    )


if __name__ == "__main__":
    main()  