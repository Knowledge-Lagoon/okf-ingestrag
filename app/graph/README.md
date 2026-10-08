# Relationship Graph

The `graph` module builds relationships between documents stored in the OKF-IngestRAG knowledge catalog.

Its purpose is to move the platform beyond independent document search and toward connected knowledge discovery.

## Overview

The core ingestion pipeline creates individual OKF documents from sources such as:

- Local Markdown files
- Confluence
- Git repositories

These documents are validated and added to:

```text
catalog/index.json
```

The relationship graph reads this catalog and identifies documents that may be related.

The current implementation creates relationships using shared tags.

Example:

```text
Kong Restart
    |
    | shared tag: kong
    |
Kong API Gateway
```

Another example:

```text
EKS Node Failure
    |
    | shared tag: kubernetes
    |
Kubernetes Pod Troubleshooting
```

## Directory Structure

```text
app/graph/
├── __init__.py
├── relationship_graph.py
└── README.md
```

The report script is located separately:

```text
scripts/
└── relationship_graph_report.py
```

## Current Data Flow

```text
Filesystem
Confluence
Git
    |
    v
OKF Documents
    |
    v
OKF Validator
    |
    v
Catalog Generator
    |
    v
catalog/index.json
    |
    v
Relationship Graph
    |
    v
Related Documents
```

## Main Component

### `relationship_graph.py`

The `RelationshipGraph` class:

1. Loads `catalog/index.json`
2. Reads each document and its tags
3. Compares every document with other documents
4. Finds shared tags
5. Creates relationships between matching documents
6. Returns an in-memory graph

Example catalog entries:

```json
[
  {
    "title": "Kong Restart",
    "type": "runbook",
    "tags": [
      "kong",
      "kubernetes",
      "restart"
    ]
  },
  {
    "title": "Kong API Gateway",
    "type": "service",
    "tags": [
      "kong",
      "api-gateway",
      "kubernetes"
    ]
  }
]
```

The graph can produce a relationship such as:

```json
{
  "Kong Restart": {
    "related": [
      {
        "document": "Kong API Gateway",
        "common_tags": [
          "kong",
          "kubernetes"
        ]
      }
    ]
  }
}
```

## Running the Graph Report

Before generating the relationship graph, ensure the catalog exists and is current:

```bash
python scripts/sync_all.py
```

Alternatively, regenerate the catalog through the main application:

```bash
python main.py
```

Run the graph report:

```bash
python scripts/relationship_graph_report.py
```

Example output:

```text
Relationship Graph
==================================================

Kong Restart
----------------------------------------
- Kong API Gateway
  Common tags: kong, kubernetes

EKS Node Failure
----------------------------------------
- Kubernetes Pod Troubleshooting
  Common tags: eks, kubernetes
```

## Relationship Rules

Relationship Graph V1 uses tag intersection.

Two documents are related when they share at least one tag.

The relationship rule is:

```text
document A tags ∩ document B tags != empty
```

Example:

```text
Document A:
tags = [kong, kubernetes, restart]

Document B:
tags = [kong, api-gateway, kubernetes]
```

Shared tags:

```text
[kong, kubernetes]
```

Therefore, the documents are related.

## Relationship Strength

A simple relationship strength can be calculated from the number of shared tags.

Example:

```text
1 shared tag  = weak relationship
2 shared tags = medium relationship
3+ shared tags = strong relationship
```

This is a suggested interpretation for future versions. Relationship Graph V1 currently identifies shared tags but does not need to classify relationship strength.

## Current Graph Model

The current implementation returns a dictionary where:

- Each document title is a node
- Each related document is another node
- Shared tags explain the connection

Example:

```python
{
    "Kong Restart": {
        "related": [
            {
                "document": "Kong API Gateway",
                "common_tags": [
                    "kong"
                ]
            }
        ]
    }
}
```

## Nodes

A node represents a valid OKF document from the catalog.

Examples:

```text
Kong Restart
Kong API Gateway
EKS Node Failure
CrashLoopBackOff
ImagePullBackOff
```

## Edges

An edge represents a relationship between two documents.

In V1, an edge is created from shared tags.

Example:

```text
Kong Restart --[kong]--> Kong API Gateway
```

## Source Data

The graph currently uses:

```text
catalog/index.json
```

The catalog may contain documents imported from:

```text
manual
confluence
git
```

The graph does not directly read raw files from connector staging directories.

Raw staging paths such as these should remain excluded from the catalog:

```text
knowledge/confluence/
knowledge/git/
```

Converted OKF documents are read from locations such as:

```text
knowledge/runbooks/
knowledge/services/
knowledge/kubernetes/
knowledge/imported/
```

## Why the Relationship Graph Is Needed

Normal search returns documents that match a query.

Example:

```text
Query: kong
```

Results:

```text
Kong Restart
Kong API Gateway
```

The relationship graph explains how those results are connected.

Example:

```text
Kong Restart
    |
    +-- related through tag: kong
    |
Kong API Gateway
```

This enables future capabilities such as:

- Related-document recommendations
- Service knowledge views
- Dependency navigation
- Knowledge exploration
- Service impact analysis
- Context expansion for LLM prompts
- Graph-assisted retrieval
- Hybrid search and RAG

## Relationship Graph and Service Catalog

The Service Catalog groups documents around a service.

Example:

```text
Service: Kong
├── Kong Restart
└── Kong API Gateway
```

The Relationship Graph finds broader connections using metadata.

Example:

```text
Kong Restart
├── Kong API Gateway
├── Kubernetes Pod Troubleshooting
└── ImagePullBackOff Recovery
```

The two modules are complementary:

```text
Service Catalog
    = service-oriented grouping

Relationship Graph
    = metadata-oriented connections
```

## Relationship Graph and RAG

The graph can later improve retrieval by expanding the initial search result.

Example:

```text
User question
    |
    v
Search finds Kong Restart
    |
    v
Graph finds related documents
    |
    +-- Kong API Gateway
    +-- Kubernetes Pod Troubleshooting
    |
    v
Relevant context sent to the LLM
```

This can provide more focused context than sending unrelated document chunks to the model.

## Limitations of V1

The current implementation has several intentional MVP limitations.

### Exact tag matching

Tags must match exactly.

These tags are treated as different:

```text
kubernetes
k8s
```

Future versions can add tag aliases or normalization.

### Generic tags

Generic tags such as:

```text
imported
confluence
git
```

may create relationships that are not operationally meaningful.

Future versions should ignore source or ingestion tags when creating domain relationships.

Suggested ignored tags:

```python
{
    "imported",
    "confluence",
    "git",
    "manual"
}
```

### Duplicate titles

The document title is currently used as the node identifier.

If two documents have the same title, one graph entry may overwrite another.

A future version should use a stable document identifier, such as:

```text
source + path
```

or:

```text
document_id
```

### Performance

The initial implementation compares every document with every other document.

Its approximate complexity is:

```text
O(n²)
```

This is acceptable for the MVP but should be optimized before using the graph with a large catalog.

### No persisted graph

The graph is currently generated in memory.

Future versions may persist it as:

```text
catalog/relationship_graph.json
```

or store it in a graph database if required.

## Recommended Metadata Improvements

For stronger relationships, OKF documents should eventually include fields such as:

```yaml
service: kong
environment:
  - production
technology:
  - kubernetes
  - api-gateway
depends_on:
  - eks
related_documents:
  - kong-restart
```

This enables explicit relationships instead of relying only on title and tag matching.

## Future Roadmap

### V1

```text
Shared-tag relationships
Console report
```

### V2

```text
Ignored generic tags
Relationship score
Document IDs
Relationship type
Persisted graph JSON
```

### V3

```text
Explicit service relationships
Dependency relationships
Owner and source relationships
Graph-assisted search
```

### V4

```text
Service impact analysis
Graph-enhanced RAG
Agentic knowledge navigation
Optional graph database integration
```

## Suggested V2 Graph Entry

```json
{
  "source_document": {
    "id": "manual:knowledge/runbooks/kong-restart.md",
    "title": "Kong Restart"
  },
  "target_document": {
    "id": "manual:knowledge/services/kong-service.md",
    "title": "Kong API Gateway"
  },
  "relationship": {
    "type": "shared_tags",
    "common_tags": [
      "kong",
      "kubernetes"
    ],
    "score": 2
  }
}
```

## Troubleshooting

### Catalog file not found

Run:

```bash
python scripts/sync_all.py
```

or:

```bash
python main.py
```

Confirm that this file exists:

```text
catalog/index.json
```

### No relationships found

Verify that documents contain overlapping tags.

Example:

```yaml
tags:
  - kong
  - kubernetes
```

Also verify that the generated catalog includes those tags.

### Raw Confluence files appear as invalid

Raw imported files are staging files and do not contain OKF frontmatter.

They should be stored under:

```text
knowledge/confluence/
```

and excluded by the catalog generator.

The converted files should be stored under:

```text
knowledge/imported/
```

### Duplicate or unexpected relationships

Check for generic shared tags such as:

```text
imported
confluence
git
```

These tags can create technically valid but low-value relationships.

Add ignored-tag filtering in Relationship Graph V2.

## Testing Recommendations

Tests should cover:

- Two documents with one common tag
- Two documents with multiple common tags
- Documents with no common tags
- Documents with missing tags
- Empty catalogs
- Duplicate document titles
- Generic tags that should be ignored
- Deterministic ordering of relationships

Suggested test location:

```text
tests/graph/
└── test_relationship_graph.py
```

## Summary

The `graph` module connects independently ingested OKF documents using shared metadata.

It currently provides:

```text
OKF Catalog
    ↓
Shared Tag Analysis
    ↓
Document Relationships
    ↓
Relationship Report
```

It forms the foundation for future service relationships, dependency mapping, graph-assisted retrieval, impact analysis, and richer AI context selection.