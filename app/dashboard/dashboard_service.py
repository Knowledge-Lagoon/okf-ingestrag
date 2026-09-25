import json
from pathlib import Path

from app.governance.analyzer import (
    KnowledgeAnalyzer
)

from app.catalog.service_catalog import (
    ServiceCatalog
)


class DashboardService:

    def __init__(self):

        self.analyzer = (
            KnowledgeAnalyzer()
        )

        self.service_catalog = (
            ServiceCatalog()
        )

        self.services = (
            self.service_catalog.build()
        )

    def _relationship_metrics(self):

        graph_file = Path(
            "catalog/relationship_graph.json"
        )

        if not graph_file.exists():

            return {
                "nodes": 0,
                "relationships": 0
            }

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as f:

            graph = json.load(f)

        nodes = len(graph)

        relationships = 0

        for node in graph.values():

            relationships += len(
                node.get(
                    "related",
                    []
                )
            )

        return {
            "nodes": nodes,
            "relationships": relationships
        }

    def _recommendation_metrics(self):

        graph_file = Path(
            "catalog/relationship_graph.json"
        )

        if not graph_file.exists():

            return 0

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as f:

            graph = json.load(f)

        recommendation_count = 0

        for node in graph.values():

            recommendation_count += len(
                node.get(
                    "related",
                    []
                )
            )

        return recommendation_count

    def build(self):

        relationship_metrics = (
            self._relationship_metrics()
        )

        dashboard = {

            #
            # Knowledge Estate
            #
            "documents": (
                self.analyzer.total_documents()
            ),

            #
            # Quality
            #
            "quality_score": (
                self.analyzer.quality_score()
            ),

            "duplicates": len(
                self.analyzer.duplicate_titles()
            ),

            "missing_owners": len(
                self.analyzer.missing_owners()
            ),

            "missing_tags": len(
                self.analyzer.missing_tags()
            ),

            "missing_descriptions": len(
                self.analyzer
                .missing_descriptions()
            ),

            #
            # Sources
            #
            "sources": (
                self.analyzer.documents_by_source()
            ),

            #
            # Services
            #
            "services": len(
                self.services
            ),

            "service_names": sorted(
                list(
                    self.services.keys()
                )
            ),

            #
            # Relationships
            #
            "graph_nodes": (
                relationship_metrics[
                    "nodes"
                ]
            ),

            "relationships": (
                relationship_metrics[
                    "relationships"
                ]
            ),

            #
            # Recommendations
            #
            "recommendations": (
                self._recommendation_metrics()
            )
        }

        return dashboard

    def platform_status(self):

        score = (
            self.analyzer
            .quality_score()
        )

        if score >= 90:

            return "HEALTHY"

        if score >= 75:

            return "WARNING"

        return "CRITICAL"