import json


class RelationshipGraph:

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

        graph = {}

        for doc in self.catalog:

            title = doc.get(
                "title",
                ""
            )

            tags = doc.get(
                "tags",
                []
            )

            graph[title] = {
                "related": []
            }

            for other_doc in self.catalog:

                if title == other_doc[
                    "title"
                ]:
                    continue

                common_tags = (
                    set(tags)
                    &
                    set(
                        other_doc.get(
                            "tags",
                            []
                        )
                    )
                )

                if common_tags:

                    graph[
                        title
                    ][
                        "related"
                    ].append(
                        {
                            "document":
                            other_doc[
                                "title"
                            ],
                            "common_tags":
                            list(
                                common_tags
                            )
                        }
                    )

        return graph