# OKF-IngestRAG User Guide

## Overview

OKF-IngestRAG is a governed enterprise knowledge platform for ingesting, validating, cataloguing, searching, connecting, and retrieving operational knowledge.

The platform currently supports knowledge from:

- Local Markdown files
- Confluence
- Git repositories

It provides:

- OKF document validation
- Dynamic catalog generation
- Keyword and content search
- Query routing
- Document retrieval
- Knowledge governance
- Service views
- Relationship graphs
- Recommendations
- Context packages
- Traceable responses with sources

Vector and semantic retrieval are planned as a later enhancement and are not enabled in release `1.1.0`.

---

## Intended Users

This guide is intended for:

- DevOps engineers
- Platform engineers
- Support engineers
- Knowledge owners
- Technical leads
- Developers maintaining OKF-IngestRAG

---

## Prerequisites

Before using the platform, confirm that:

- Python and project dependencies are installed
- The repository is checked out locally
- The current working directory is the repository root
- At least one valid OKF Markdown document exists
- Required environment variables are configured for external connectors

Activate the project virtual environment if one is used:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Knowledge Document Format

Every searchable document must contain YAML frontmatter followed by Markdown content.

Example:

```markdown
---
type: runbook
title: Kong Restart
description: Procedure to restart Kong in Kubernetes
tags:
  - kong
  - kubernetes
  - restart
owner: devops
source: manual
version: 1.0
---

# Kong Restart

Restart the deployment:

```bash
kubectl rollout restart deployment kong -n kong
```
```

Required project metadata:

- `type`
- `title`
- `description`
- `tags`
- `owner`

Recommended metadata:

- `source`
- `version`
- `service`

---

## Knowledge Directory Structure

Typical structure:

```text
knowledge/
├── runbooks/
├── services/
├── kubernetes/
├── imported/
├── confluence/
└── git/
```

Directory purposes:

- `runbooks/`: manually maintained operational procedures
- `services/`: service descriptions and ownership information
- `kubernetes/`: Kubernetes references and troubleshooting knowledge
- `imported/`: OKF-converted documents imported from external systems
- `confluence/`: raw Confluence staging files
- `git/`: raw Git staging files, if configured

Raw staging files are not intended to be indexed directly.

---

## Running the Platform

### Refresh the catalog and platform metrics

```bash
python scripts/platform_sync.py
```

This refreshes the generated knowledge catalog and executes platform-level analysis.

### Run the main knowledge assistant

```bash
python main.py
```

### Run the single query interface

```bash
python scripts/query.py
```

Example:

```text
Ask a question: kong
```

Expected output includes:

- Matching source documents
- Source paths
- Related knowledge
- Retrieval trace

Type `exit` or `quit` to close the query interface.

---

## Searching Knowledge

The current release uses keyword, metadata, content, and relationship-based retrieval.

Example query:

```text
kong
```

Possible result:

```text
Kong API Gateway
Kong Restart
```

The response includes source attribution such as:

```text
Title : Kong Restart
Source: manual
Path  : knowledge/runbooks/kong-restart.md
```

### Why source attribution matters

The source section shows where retrieved knowledge originated. This allows users to verify the evidence rather than relying on an unexplained generated answer.

---

## Importing Confluence Knowledge

### Configure environment variables

```bash
export CONFLUENCE_USERNAME="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_PAGE_ID="786433"
export CONFLUENCE_SPACE_KEY="YOUR_SPACE_KEY"
```

Do not commit credentials or tokens to Git.

### Test Confluence connectivity

```bash
python scripts/test_confluence.py
```

A successful result displays the page ID and title.

### Import one Confluence page

```bash
python scripts/import_confluence_page.py
```

The flow is:

```text
Confluence page
    ↓
Raw local export
    ↓
OKF conversion
    ↓
knowledge/imported/
```

### Import a Confluence space

```bash
python scripts/import_confluence_space.py
```

If the space-listing endpoint returns `403` or `404`, verify the space key and the API user's permissions. Single-page import can still be used when space enumeration is unavailable.

### Refresh after import

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
```

---

## Importing Git Knowledge

Configure the repository path in the Git import script or associated configuration.

Run:

```bash
python scripts/import_git_repo.py
```

The connector discovers supported documentation, copies it into the staging area, converts it to OKF, and places searchable documents under `knowledge/imported/`.

Refresh generated artifacts:

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
```

---

## Governance Report

Run:

```bash
python scripts/knowledge_report.py
```

The report displays:

- Total documents
- Documents by type
- Documents by source
- Duplicate titles
- Missing owners
- Missing tags
- Missing descriptions
- Knowledge quality score

A release-ready knowledge set should have no unexpected metadata gaps or duplicate titles.

---

## Service Overview

Run:

```bash
python scripts/service_overview.py
```

The service overview groups knowledge into:

- Runbooks
- Documentation
- Owners
- Sources
- Tags

Current limitation:

The MVP derives the service name from the first word of a document title. This can produce service names such as `Overview`, `Getting`, or `Readme`. A future release should use explicit metadata:

```yaml
service: kong
```

---

## Relationship Graph

Build the graph:

```bash
python scripts/build_graph.py
```

View relationships:

```bash
python scripts/relationship_graph_report.py
```

The graph connects documents that share meaningful tags. Generic tags such as `imported`, `confluence`, `git`, and `manual` should be ignored by graph logic.

Generated artifact:

```text
catalog/relationship_graph.json
```

---

## Recommendations

Run:

```bash
python scripts/recommendation_report.py
```

The recommendation engine uses graph relationships to suggest additional knowledge for a selected document.

No recommendation is returned when no meaningful graph relationship exists.

---

## Context Packages

Run:

```bash
python scripts/context_report.py
```

A context package can include:

- The original query
- Primary document
- Document type
- Source
- Related documents
- Service information
- Owners
- Tags

Context packages are designed for deterministic assistant responses and future LLM consumption.

---

## Dashboard

Run:

```bash
python scripts/dashboard.py
```

The dashboard displays:

- Total documents
- Knowledge sources
- Quality score
- Missing metadata counts
- Duplicate count
- Service count
- Graph node count
- Relationship count
- Recommendation paths
- Overall platform status

Platform status thresholds:

- `HEALTHY`: quality score of 90 or above
- `WARNING`: quality score from 75 to below 90
- `CRITICAL`: quality score below 75

---

## Generated Artifacts

The platform generates:

```text
catalog/index.json
catalog/relationship_graph.json
```

These are generated artifacts and should not be edited manually.

The Markdown knowledge files are the source of truth.

---

## Recommended Operating Sequence

For a normal refresh and validation cycle:

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
python scripts/knowledge_report.py
python scripts/dashboard.py
python scripts/query.py
```

For source ingestion, run the appropriate connector before platform synchronization.

---

## Known Limitations in Version 1.1.0

- Vector semantic retrieval is not enabled
- `Vector Matches` in the query trace is expected to be `0`
- Service names are inferred from titles
- Confluence space enumeration depends on API permissions and space availability
- No REST API or web UI
- No authentication or document-level authorization
- No scheduled synchronization
- Remote Ollama generation is not part of the validated release path

---

## Common Problems

### No search results

Confirm the catalog is current:

```bash
python scripts/platform_sync.py
```

Confirm the query matches a title, tag, type, description, or document content.

### Missing catalog

```bash
python scripts/platform_sync.py
```

### Missing graph

```bash
python scripts/build_graph.py
```

### Raw Confluence files reported as invalid

Raw files under `knowledge/confluence/` do not contain OKF frontmatter. Use the converted versions under `knowledge/imported/`.

### Query interface import error

Version `1.1.0` must use the non-vector `HybridRetriever` implementation. It uses keyword search and graph expansion while vector retrieval remains disabled.

See `docs/troubleshooting.md` for additional diagnostics.

---

## User Acceptance Checklist

The platform is ready for use when:

- The catalog contains at least one document
- The governance report runs without exceptions
- The relationship graph builds successfully
- The dashboard reports platform health
- Query output includes document sources and paths
- No unexpected metadata gaps remain

---

## Further Reading

- `README.md`
- `docs/architecture.md`
- `docs/data-flow.md`
- `docs/deployment.md`
- `docs/testing.md`
- `docs/troubleshooting.md`
- `docs/roadmap.md`
