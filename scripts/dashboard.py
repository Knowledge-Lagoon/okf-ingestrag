print("STARTING DASHBOARD")

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

from app.dashboard.dashboard_service import (
    DashboardService
)


def main():

    dashboard = (
        DashboardService()
    )

    data = dashboard.build()

    print(
        "\nKnowledge Dashboard"
    )

    print(
        "=" * 60
    )

    #
    # Knowledge Estate
    #
    print(
        "\nKnowledge Estate"
    )

    print(
        "-" * 30
    )

    print(
        f"Total Documents: "
        f"{data['documents']}"
    )

    #
    # Sources
    #
    print(
        "\nSources"
    )

    print(
        "-" * 30
    )

    for (
        source,
        count
    ) in data[
        "sources"
    ].items():

        print(
            f"{source}: {count}"
        )

    #
    # Quality
    #
    print(
        "\nKnowledge Quality"
    )

    print(
        "-" * 30
    )

    print(
        f"Quality Score: "
        f"{data['quality_score']}%"
    )

    print(
        f"Missing Owners: "
        f"{data['missing_owners']}"
    )

    print(
        f"Missing Tags: "
        f"{data['missing_tags']}"
    )

    print(
        f"Missing Descriptions: "
        f"{data['missing_descriptions']}"
    )

    print(
        f"Duplicates: "
        f"{data['duplicates']}"
    )

    #
    # Services
    #
    print(
        "\nServices"
    )

    print(
        "-" * 30
    )

    print(
        f"Total Services: "
        f"{data['services']}"
    )

    for service in data[
        "service_names"
    ]:

        print(
            f"- {service}"
        )

    #
    # Graph
    #
    print(
        "\nRelationship Graph"
    )

    print(
        "-" * 30
    )

    print(
        f"Graph Nodes: "
        f"{data['graph_nodes']}"
    )

    print(
        f"Relationships: "
        f"{data['relationships']}"
    )

    #
    # Recommendations
    #
    print(
        "\nRecommendations"
    )

    print(
        "-" * 30
    )

    print(
        f"Recommendation Paths: "
        f"{data['recommendations']}"
    )

    #
    # Platform Health
    #
    print(
        "\nPlatform Health"
    )

    print(
        "-" * 30
    )

    print(
        dashboard.platform_status()
    )

    print(
        "\nDashboard Complete\n"
    )


if __name__ == "__main__":
    main()