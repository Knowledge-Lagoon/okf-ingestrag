from app.catalog.generator import (
    CatalogGenerator
)

from app.governance.report import (
    KnowledgeReport
)


class IngestionPipeline:

    @staticmethod
    def run():

        print(
            "\nRefreshing catalog...\n"
        )

        catalog = (
            CatalogGenerator.generate()
        )

        print(
            f"Catalog entries: "
            f"{len(catalog)}"
        )

        print(
            "\nGenerating governance report...\n"
        )

        KnowledgeReport.generate()

        print(
            "\nPipeline Complete"
        )