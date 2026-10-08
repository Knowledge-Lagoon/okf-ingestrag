# Dashboard Module

The Dashboard module provides a consolidated operational view of the OKF-IngestRAG knowledge platform.

It aggregates metrics from the catalog, governance engine, Service Catalog, Relationship Graph, and recommendation data into a single platform health summary.

---

## Purpose

OKF-IngestRAG contains several independent reporting capabilities:

```text
Knowledge Governance
Service Catalog
Relationship Graph
Recommendation Engine
```

During development, these can be executed separately:

```bash
python scripts/knowledge_report.py
python scripts/service_overview.py
python scripts/relationship_graph_report.py
python scripts/recommendation_report.py
```

The Dashboard module combines their key metrics into one operational view.

It answers questions such as:

- How many valid knowledge documents exist?
- Which sources provide the knowledge?
- What is the overall knowledge quality score?
- Are any documents missing owners, tags, or descriptions?
- How many services have been identified?
- How many graph nodes and relationships exist?
- How many recommendation paths are available?
- What is the overall platform health?

---

## Module Structure

```text
app/dashboard/
├── __init__.py
├── dashboard_service.py
└── README.md
```

The command-line entry point is:

```text
scripts/
└── dashboard.py
```

---

## Architecture

```text
Knowledge Sources
=================

Filesystem
Confluence
Git

        ↓

OKF Conversion

        ↓

Validation

        ↓

Catalog

        ↓

┌───────────────────────────────┐
│      Dashboard Service        │
├───────────────────────────────┤
│ Governance Metrics            │
│ Service Catalog Metrics       │
│ Relationship Graph Metrics    │
│ Recommendation Metrics        │
└───────────────────────────────┘

        ↓

Knowledge Dashboard
```

---

## Main Components

### `dashboard_service.py`

The `DashboardService` is responsible for collecting and aggregating platform metrics.

It uses:

```text
KnowledgeAnalyzer
ServiceCatalog
relationship_graph.json
```

The service returns a dictionary containing dashboard data.

Example:

```python
{
    "documents": 13,
    "quality_score": 96.15,
    "duplicates": 1,
    "missing_owners": 0,
    "missing_tags": 0,
    "missing_descriptions": 0,
    "sources": {
        "manual": 5,
        "confluence": 6,
        "git": 2
    },
    "services": 4,
    "service_names": [
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "Kong",
        "Terraform"
    ],
    "graph_nodes": 13,
    "relationships": 27,
    "recommendations": 27
}
```

### `scripts/dashboard.py`

The dashboard script provides a command-line view of the aggregated data.

It formats the data returned by `DashboardService` into readable sections.

---

## Data Sources

The Dashboard uses generated platform artifacts rather than reading raw connector content directly.

### Knowledge Catalog

```text
catalog/index.json
```

Provides:

- Total documents
- Document types
- Knowledge sources
- Metadata quality
- Duplicate titles
- Service information

### Relationship Graph

```text
catalog/relationship_graph.json
```

Provides:

- Graph node count
- Relationship count
- Recommendation path count

### Governance Analyzer

```text
app/governance/analyzer.py
```

Provides:

- Knowledge quality score
- Missing owners
- Missing tags
- Missing descriptions
- Duplicate titles
- Documents by source

### Service Catalog

```text
app/catalog/service_catalog.py
```

Provides:

- Total services
- Service names
- Runbooks by service
- Documentation by service
- Owners, tags, and sources

---

## Dashboard Sections

### Knowledge Estate

Reports the total number of valid OKF documents in the generated catalog.

Example:

```text
Knowledge Estate
------------------------------
Total Documents: 13
```

Only documents included in `catalog/index.json` are counted.

Raw connector staging files should not be included.

---

### Sources

Reports how knowledge is distributed across supported sources.

Example:

```text
Sources
------------------------------
manual: 5
confluence: 6
git: 2
```

Sources originate from the `source` field in OKF metadata.

Example:

```yaml
source: confluence
```

If a source is not specified, the Catalog Generator currently defaults it to:

```text
manual
```

---

### Knowledge Quality

Reports the overall health of document metadata.

Example:

```text
Knowledge Quality
------------------------------
Quality Score: 96.15%
Missing Owners: 0
Missing Tags: 0
Missing Descriptions: 0
Duplicates: 1
```

The current quality score evaluates:

- Owner presence
- Tag presence
- Description presence

Each document has three quality checks.

Conceptually:

```text
Quality Score =
Completed Metadata Checks
÷
Total Metadata Checks
×
100
```

Duplicate titles are reported separately and do not currently reduce the quality score.

---

### Services

Reports service groupings produced by the Service Catalog.

Example:

```text
Services
------------------------------
Total Services: 4
- CrashLoopBackOff
- ImagePullBackOff
- Kong
- Terraform
```

The current Service Catalog MVP derives a service name using the first word of the document title.

Example:

```text
Kong Restart
Kong API Gateway
```

Both are grouped under:

```text
Kong
```

This is an MVP rule. A later version should use explicit service metadata:

```yaml
service: kong
```

---

### Relationship Graph

Reports graph metrics from:

```text
catalog/relationship_graph.json
```

Example:

```text
Relationship Graph
------------------------------
Graph Nodes: 13
Relationships: 27
```

A node represents a catalog document.

A relationship represents a connection between two documents, currently based on shared non-generic tags.

Example:

```text
Kong Restart
      |
      | shared tags: kong, kubernetes
      |
Kong API Gateway
```

---

### Recommendations

Reports the number of available recommendation paths.

Example:

```text
Recommendations
------------------------------
Recommendation Paths: 27
```

Relationship Graph V2 stores directed related-document entries.

Therefore, if two documents reference each other, the dashboard may count both directions:

```text
Document A → Document B
Document B → Document A
```

The current recommendation count represents available graph-based recommendation paths, not necessarily the number of unique undirected document relationships.

---

### Platform Health

The Dashboard calculates a simple platform health status using the governance quality score.

Current thresholds:

```text
90 or above:
HEALTHY

75 to below 90:
WARNING

Below 75:
CRITICAL
```

Example:

```text
Platform Health
------------------------------
HEALTHY
```

This is an MVP health indicator. Future versions can include additional factors such as:

- Catalog availability
- Graph freshness
- Connector sync failures
- Duplicate rate
- Missing ownership
- Stale documents
- LLM endpoint availability

---

## Running the Dashboard

Before running the Dashboard, ensure the catalog and relationship graph are current.

### Refresh the catalog

```bash
python scripts/platform_sync.py
```

Alternatively:

```bash
python main.py
```

### Build the relationship graph

```bash
python scripts/build_graph.py
```

### Run the Dashboard

```bash
python scripts/dashboard.py
```

---

## Example Output

```text
STARTING DASHBOARD

Knowledge Dashboard
============================================================

Knowledge Estate
------------------------------
Total Documents: 13

Sources
------------------------------
manual: 5
confluence: 6
git: 2

Knowledge Quality
------------------------------
Quality Score: 96.15%
Missing Owners: 0
Missing Tags: 0
Missing Descriptions: 0
Duplicates: 1

Services
------------------------------
Total Services: 4
- CrashLoopBackOff
- ImagePullBackOff
- Kong
- Terraform

Relationship Graph
------------------------------
Graph Nodes: 13
Relationships: 27

Recommendations
------------------------------
Recommendation Paths: 27

Platform Health
------------------------------
HEALTHY

Dashboard Complete
```

---

## Programmatic Usage

The Dashboard can also be consumed directly from Python.

```python
from app.dashboard.dashboard_service import (
    DashboardService
)


dashboard_service = DashboardService()

dashboard = dashboard_service.build()

print(
    dashboard["documents"]
)

print(
    dashboard["quality_score"]
)

print(
    dashboard_service.platform_status()
)
```

---

## Example JSON Representation

```python
import json

from app.dashboard.dashboard_service import (
    DashboardService
)


service = DashboardService()

data = service.build()

print(
    json.dumps(
        data,
        indent=4
    )
)
```

Example output:

```json
{
    "documents": 13,
    "quality_score": 96.15,
    "duplicates": 1,
    "missing_owners": 0,
    "missing_tags": 0,
    "missing_descriptions": 0,
    "sources": {
        "manual": 5,
        "confluence": 6,
        "git": 2
    },
    "services": 4,
    "service_names": [
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "Kong",
        "Terraform"
    ],
    "graph_nodes": 13,
    "relationships": 27,
    "recommendations": 27
}
```

This structured output can later be exposed through a REST API.

---

## Platform Service Integration

The Dashboard should eventually be exposed through the Platform Service.

Example future interface:

```python
from app.platform.platform_service import (
    PlatformService
)


platform = PlatformService()

dashboard = platform.dashboard()
```

This allows the application to use one orchestration layer instead of calling dashboard components directly.

Future flow:

```text
Application
     |
     v
Platform Service
     |
     v
Dashboard Service
     |
     v
Governance + Catalog + Graph Metrics
```

---

## Future API Integration

The Dashboard Service is designed to support a future FastAPI endpoint.

Example:

```http
GET /api/v1/dashboard
```

Possible response:

```json
{
    "status": "HEALTHY",
    "documents": 13,
    "quality_score": 96.15,
    "services": 4,
    "graph_nodes": 13,
    "relationships": 27
}
```

The API layer should call `DashboardService` rather than reimplementing dashboard calculations.

---

## Future User Interface

A future web interface could display:

```text
┌─────────────────────────────┐
│ Total Documents             │
│ 13                          │
├─────────────────────────────┤
│ Knowledge Quality           │
│ 96.15%                      │
├─────────────────────────────┤
│ Services                    │
│ 4                           │
├─────────────────────────────┤
│ Relationships               │
│ 27                          │
└─────────────────────────────┘
```

Additional visualizations could include:

- Documents by source
- Documents by type
- Quality issues by category
- Top services
- Top tags
- Knowledge growth over time
- Connector sync status
- Relationship density
- Documents without relationships

These are roadmap items and are not implemented in Dashboard V1.

---

## Error Handling

The Dashboard should handle missing generated artifacts gracefully.

### Missing relationship graph

If this file does not exist:

```text
catalog/relationship_graph.json
```

the Dashboard currently returns:

```python
{
    "nodes": 0,
    "relationships": 0
}
```

The catalog and governance analyzer must still be available for the remaining Dashboard sections.

### Missing catalog

If this file does not exist:

```text
catalog/index.json
```

regenerate it using:

```bash
python scripts/platform_sync.py
```

or:

```bash
python main.py
```

### Invalid JSON

If a generated JSON file is malformed, the Dashboard may raise a JSON decoding error.

Regenerate the affected artifact rather than manually editing generated output.

---

## Operational Workflow

Recommended execution order:

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
python scripts/dashboard.py
```

A later Platform Service version should combine these into one operation:

```bash
python main.py sync
```

Target flow:

```text
Knowledge Import
       ↓
OKF Conversion
       ↓
Validation
       ↓
Catalog Refresh
       ↓
Graph Refresh
       ↓
Governance Analysis
       ↓
Dashboard
```

---

## Testing

Recommended test structure:

```text
tests/
└── dashboard/
    └── test_dashboard_service.py
```

Tests should cover:

- Empty catalog
- Catalog with one document
- Multiple knowledge sources
- Missing metadata
- Duplicate titles
- Missing relationship graph
- Empty relationship graph
- Multiple graph relationships
- Healthy platform score
- Warning platform score
- Critical platform score

Example:

```python
from app.dashboard.dashboard_service import (
    DashboardService
)


def test_platform_status():

    service = DashboardService()

    status = service.platform_status()

    assert status in {
        "HEALTHY",
        "WARNING",
        "CRITICAL"
    }
```

For deterministic testing, Dashboard dependencies should eventually support injected catalog and graph file paths.

---

## Current Limitations

Dashboard V1 has the following limitations:

- Command-line output only
- No historical trend storage
- No interactive visualizations
- No connector sync status
- No source freshness tracking
- No document review-date tracking
- No persisted Dashboard snapshot
- Relationship count may include both relationship directions
- Recommendation count currently mirrors graph relationship paths
- Service identification is based on title parsing
- No authentication or authorization layer
- No API endpoint
- No web interface

These limitations are acceptable for the current MVP.

---

## Security Considerations

The Dashboard currently displays aggregate metadata and service names.

Future deployments should consider:

- User authentication
- Role-based dashboard access
- Document-level authorization
- Sensitive service-name masking
- Audit logging
- Secure API access
- Avoiding exposure of document content
- Tenant and source isolation

The Dashboard should not reveal knowledge metadata that the requesting user is not authorized to view.

---

## Recommended Enhancements

### Dashboard V2

```text
Documents by type
Top tags
Relationship density
Orphan documents
Connector sync status
```

### Dashboard V3

```text
Historical quality trends
Knowledge growth trends
Source freshness
Document review status
```

### Dashboard V4

```text
FastAPI endpoints
Web dashboard
Interactive graph visualization
Service drill-down
```

### Dashboard V5

```text
AI-generated knowledge health summaries
Recommended remediation actions
Governance alerts
```

---

## Relationship With Other Modules

### Governance

Provides quality and metadata completeness metrics.

```text
app/governance/
```

### Catalog

Provides the searchable knowledge inventory.

```text
app/catalog/
```

### Service Catalog

Provides service names and service groupings.

```text
app/catalog/service_catalog.py
```

### Relationship Graph

Provides graph node and link metrics.

```text
app/graph/
```

### Recommendations

Uses graph relationships to identify useful next knowledge.

```text
app/recommendations/
```

### Platform Service

Coordinates platform refresh and should eventually expose Dashboard operations.

```text
app/platform/
```

---

## Summary

The Dashboard module provides a consolidated view of the OKF-IngestRAG platform.

It combines:

```text
Knowledge Inventory
        +
Knowledge Quality
        +
Service Awareness
        +
Knowledge Relationships
        +
Recommendation Coverage
```

into a single operational report.

Dashboard V1 is the foundation for future API-driven and web-based platform observability.
