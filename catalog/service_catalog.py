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

            title = doc["title"]

            service_name = (
                title.split()[0]
            )

            if service_name not in services:

                services[service_name] = []

            services[service_name].append(
                title
            )

        return services