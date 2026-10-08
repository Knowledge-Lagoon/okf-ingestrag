import json


class ServiceCatalog:

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

    def build(self):

        services = {}

        for doc in self.catalog:

            title = doc.get(
                "title",
                ""
            )

            if not title:
                continue

            #
            # Simple service identification:
            # First word of title.
            #
            service_name = (
                title.split()[0]
            )

            if (
                service_name
                not in services
            ):

                services[
                    service_name
                ] = {
                    "runbooks": [],
                    "documentation": [],
                    "sources": set(),
                    "owners": set(),
                    "tags": set(),
                    "documents": []
                }

            service = services[
                service_name
            ]

            document_type = (
                doc.get(
                    "type",
                    ""
                )
                .lower()
            )

            #
            # Categorize document.
            #
            if document_type == "runbook":

                service[
                    "runbooks"
                ].append(title)

            else:

                service[
                    "documentation"
                ].append(title)

            #
            # Track all documents.
            #
            service[
                "documents"
            ].append(
                title
            )

            #
            # Track ownership.
            #
            service[
                "owners"
            ].add(
                doc.get(
                    "owner",
                    "unknown"
                )
            )

            #
            # Track sources.
            #
            service[
                "sources"
            ].add(
                doc.get(
                    "source",
                    "manual"
                )
            )

            #
            # Track tags.
            #
            for tag in doc.get(
                "tags",
                []
            ):

                service[
                    "tags"
                ].add(tag)

        #
        # Convert sets to sorted lists
        #
        for service in services.values():

            service[
                "runbooks"
            ] = sorted(
                service[
                    "runbooks"
                ]
            )

            service[
                "documentation"
            ] = sorted(
                service[
                    "documentation"
                ]
            )

            service[
                "documents"
            ] = sorted(
                service[
                    "documents"
                ]
            )

            service[
                "owners"
            ] = sorted(
                list(
                    service[
                        "owners"
                    ]
                )
            )

            service[
                "sources"
            ] = sorted(
                list(
                    service[
                        "sources"
                    ]
                )
            )

            service[
                "tags"
            ] = sorted(
                list(
                    service[
                        "tags"
                    ]
                )
            )

        return services

    def get_service(
        self,
        service_name
    ):

        services = self.build()

        return services.get(
            service_name,
            {}
        )

    def list_services(self):

        services = self.build()

        return sorted(
            services.keys()
        )