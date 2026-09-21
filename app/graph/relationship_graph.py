import json


class RelationshipGraph:

    IGNORED_TAGS = {
        "git",
        "confluence",
        "imported",
        "manual"
    }

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

    def _clean_tags(
        self,
        tags
    ):

        return {
            tag.lower()
            for tag in tags
            if tag.lower()
            not in self.IGNORED_TAGS
        }

    def build(self):

        graph = {}

        for doc in self.catalog:

            title = doc["title"]

            source_tags = self._clean_tags(
                doc.get(
                    "tags",
                    []
                )
            )

            graph[title] = {
                "related": []
            }

            for other in self.catalog:

                if (
                    other["title"]
                    == title
                ):
                    continue

                target_tags = (
                    self._clean_tags(
                        other.get(
                            "tags",
                            []
                        )
                    )
                )

                common_tags = (
                    source_tags
                    &
                    target_tags
                )

                if common_tags:

                    graph[
                        title
                    ][
                        "related"
                    ].append(
                        {
                            "document":
                            other[
                                "title"
                            ],
                            "score":
                            len(
                                common_tags
                            ),
                            "common_tags":
                            sorted(
                                list(
                                    common_tags
                                )
                            )
                        }
                    )

            graph[
                title
            ][
                "related"
            ] = sorted(
                graph[title][
                    "related"
                ],
                key=lambda x: (
                    x["score"]
                ),
                reverse=True
            )

        return graph