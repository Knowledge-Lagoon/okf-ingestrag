# OKF-IngestRAG

Enterprise Knowledge Ingestion, Governance, Discovery and AI Context Platform

---

## Overview

OKF-IngestRAG is an enterprise knowledge platform that ingests knowledge from multiple sources, converts it into the Open Knowledge Format (OKF), validates and indexes content, and builds governance, service awareness, relationship mapping, recommendations, context packages, and AI-ready retrieval capabilities.

The platform is designed to support:

- Operational knowledge
- Runbooks
- Service documentation
- Architecture guidance
- Engineering knowledge
- Support procedures
- AI-assisted knowledge retrieval

Unlike traditional RAG implementations that focus primarily on embeddings and vector databases, OKF-IngestRAG prioritizes structured, governed, traceable knowledge before introducing AI generation.

---

## Documentation

This README is the primary project reference. The following documents provide deeper guidance.

### User and Operations

- [User Guide](docs/user-guide.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

### Architecture and Design

- [Architecture](docs/architecture.md)
- [Data Flow](docs/data-flow.md)
- [Roadmap](docs/roadmap.md)

### Quality and Release

- [Testing Guide](docs/testing.md)
- [Changelog](CHANGELOG.md)
- [Version](VERSION)

### Module Documentation

- [Application Overview](app/README.md)
- [Assistant](app/assistant/README.md)
- [Catalog](app/catalog/README.md)
- [Connectors](app/connectors/README.md)
- [Context](app/context/README.md)
- [Dashboard](app/dashboard/README.md)
- [Governance](app/governance/README.md)
- [Graph](app/graph/README.md)
- [Platform](app/platform/README.md)
- [RAG](app/rag/README.md)
- [Recommendations](app/recommendations/README.md)
- [Retrieval](app/retrieval/README.md)
- [Router](app/router/README.md)
- [Search](app/search/README.md)

---

## Key Principles

### Knowledge First

Knowledge is treated as a governed asset.

```text
Knowledge
    ↓
Governance
    ↓
Discovery
    ↓
AI
```

### Open Knowledge Format

All indexed knowledge is normalized into a standard OKF structure.

Benefits:

- Consistent metadata
- Traceability
- Source attribution
- Searchability
- Governance
- AI readiness

### Explainability

Every user-facing response should expose the evidence that produced it.

```text
Answer
  +
Sources
  +
Related Knowledge
  +
Retrieval Trace
```

### Hybrid by Design

The current validated retrieval path combines:

```text
Keyword and Content Search
          +
Relationship Graph Expansion
```

Semantic vector retrieval is designed as an extension to this path, not a replacement for OKF metadata, governance, service context, or graph relationships.

### AI Ready by Design

The platform builds context and evidence packages that can be consumed by:

- Local LLMs
- Remote Ollama deployments
- Agent frameworks
- Future RAG implementations

The platform remains useful when an LLM is unavailable.

---

# Features

## Knowledge Sources

### Filesystem

Import and manage:

- Markdown
- Text documentation
- Runbooks
- Internal knowledge

### Confluence

Supports:

- API authentication
- Page retrieval
- Content extraction
- Single-page import
- Bulk space import where permissions allow
- Raw staging export
- Automatic OKF conversion

### Git Repositories

Supports:

- README files
- Documentation
- Runbooks
- Architecture guides
- Local repository document discovery
- Automatic OKF conversion

---

## Knowledge Processing

### OKF Conversion

Imported content is converted into an OKF document containing YAML frontmatter and Markdown content.

Example:

```yaml
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
```

### Validation

The validator checks:

- YAML frontmatter
- Required fields
- Metadata structure
- Document validity

Required metadata currently includes:

- `type`
- `title`
- `description`
- `tags`
- `owner`

### Catalog Generation

The catalog generator produces:

```text
catalog/index.json
```

The catalog is the generated searchable inventory of valid OKF documents. It includes metadata, source paths, and document content for retrieval.

Raw connector staging directories such as `knowledge/confluence/` and `knowledge/git/` are excluded from catalog indexing.

---

## Knowledge Discovery

### Search

Supports:

- Title matching
- Type matching
- Description matching
- Tag matching
- Full-content matching
- Optional document-type filtering

### Ranking

Search results are ranked using weighted relevance signals such as:

- Title matches
- Description matches
- Tag matches
- Content matches

### Query Routing

The router identifies whether a question is primarily about:

- Runbooks
- Services
- General knowledge

When no bounded document type is identified, the system searches across all document types.

### Keyword Extraction

The keyword extractor removes common stop words and selects useful query terms for retrieval.

### Retrieval

The retrieval layer loads the complete source document after search identifies the best candidate.

---

## Knowledge Governance

Governance V2 provides visibility into knowledge quality and completeness.

### Knowledge Health Metrics

- Total documents
- Documents by type
- Documents by source

### Quality Validation

- Missing owners
- Missing tags
- Missing descriptions

### Duplicate Detection

Detects duplicate document titles in the catalog.

### Quality Score

The quality score measures completion of owner, tag, and description metadata across catalog entries.

During release validation, the knowledge estate achieved:

```text
Total Documents: 13
Knowledge Quality Score: 100.0%
Missing Owners: 0
Missing Tags: 0
Missing Descriptions: 0
Duplicates: 0
```

---

## Service Catalog

The Service Catalog groups runbooks and documentation into service-oriented views.

Example:

```text
Kong
├── Runbooks
├── Documentation
├── Owners
├── Sources
└── Tags
```

The catalog currently captures:

- Runbooks
- Documentation
- Owners
- Sources
- Tags
- Related document titles

### Current Limitation

The MVP infers the service name from the first word of the document title. This can create service entries such as `Overview`, `Getting`, or `Readme`.

A future implementation should use explicit metadata:

```yaml
service: kong
```

---

## Relationship Graph

The Relationship Graph connects documents using shared meaningful tags.

Example:

```text
Kong Restart
      │
      └── Kong API Gateway
```

Generated artifact:

```text
catalog/relationship_graph.json
```

Relationship Graph V2 provides:

- Generic-tag filtering
- Shared-tag relationships
- Relationship scores
- Deterministic relationship ordering
- Persisted graph output

Generic source and ingestion tags such as these are ignored:

```text
imported
confluence
git
manual
```

During release validation, the graph contained:

```text
Graph Nodes: 13
Relationships: 14
```

---

## Recommendation Engine

The Recommendation Engine consumes Relationship Graph entries and returns the most relevant related knowledge.

Recommendation results include:

- Related document title
- Relationship score
- Shared tags

Recommendations are optional. Documents without meaningful relationships return an empty recommendation list rather than causing an error.

---

## Context Builder

The Context Builder combines primary and related knowledge into a structured context package.

Example:

```json
{
  "query": "Tell me about Kong",
  "primary_document": "Kong Restart",
  "document_type": "runbook",
  "source": "manual",
  "related_documents": [
    {
      "document": "Kong API Gateway",
      "score": 1,
      "common_tags": ["kong"]
    }
  ],
  "service": {
    "runbooks": ["Kong Restart"],
    "documentation": ["Kong API Gateway"],
    "owners": ["devops", "platform-team"]
  }
}
```

Context packages are designed for:

- Deterministic assistant responses
- Source-aware response generation
- Future LLM grounding
- Future API consumption

---

## Assistant

Assistant V2 provides:

- Structured responses
- Source attribution
- Service awareness
- Related knowledge
- Graph context

The assistant can operate:

- Without an LLM
- With a remote Ollama deployment
- With future AI providers

---

## Evidence and Traceability

The RAG foundation provides:

- Evidence Package
- Citation Builder
- Retrieval Trace
- Related Knowledge
- Unique Source Counting

Example query response:

```text
Question:
kong

Sources
-------
Title : Kong API Gateway
Source: manual
Path  : knowledge/services/kong-service.md

Title : Kong Restart
Source: manual
Path  : knowledge/runbooks/kong-restart.md

Related Knowledge
-----------------
- Kong Restart

Retrieval Trace
---------------
Keyword Matches: 2
Vector Matches: 0
Graph Matches: 1
Unique Sources: 2
```

This makes the retrieval result explainable even when LLM generation is not used.

---

## Hybrid Retrieval

The validated hybrid retrieval path currently combines:

```text
Keyword Search
      +
Content and Metadata Search
      +
Relationship Graph Expansion
```

### Current Behavior

- Keyword and content matches are collected from the catalog.
- The highest-ranked result is used for graph expansion.
- Graph relationships are added to the Evidence Package.
- Citations and retrieval trace are returned to the user.

### Vector Extension

The architecture supports future semantic retrieval through:

- Document chunking
- Embedding generation
- ChromaDB persistence
- SemanticRetriever
- Vector-based ranking

Semantic vector retrieval is not enabled in the validated current query path. Therefore, `Vector Matches` is expected to be `0`.

---

## Ollama Integration

The platform includes remote Ollama integration code for prompt-based generation.

Validated aspects include:

- Remote endpoint configuration
- Prompt construction
- Generation request integration
- Deterministic fallback architecture

A successful earlier run produced a response grounded in the Kong runbook content.

### Current Limitation

End-to-end grounded answer generation through Ollama was not included in the final validated query path because remote inference was subject to environment-dependent timeouts.

The stable current query path returns evidence, sources, and retrieval trace without requiring Ollama.

---

## Dashboard

The Dashboard aggregates platform metrics from:

- Catalog
- Governance
- Service Catalog
- Relationship Graph
- Recommendation paths

Release-validation output included:

```text
Total Documents: 13
Quality Score: 100.0%
Total Services: 12
Graph Nodes: 13
Relationships: 14
Recommendation Paths: 14
Platform Health: HEALTHY
```

---

## Platform Service

The Platform Service coordinates:

- Catalog refresh
- Governance reporting
- Service Catalog generation
- Relationship Graph generation

It provides the foundation for future API, scheduling, and user-interface layers.

---

# Architecture

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

Search
Ranking
Routing
Retrieval

        ↓

Governance
Service Catalog
Relationship Graph
Recommendations

        ↓

Context Builder

        ↓

Evidence Package
Citation Builder
Retrieval Trace

        ↓

Assistant

        ↓

Optional Ollama / Future LLM
```

---

# Repository Structure

```text
app/
├── assistant/
├── catalog/
├── connectors/
├── context/
├── dashboard/
├── governance/
├── graph/
├── llm/
├── okf/
├── platform/
├── rag/
├── recommendations/
├── retrieval/
├── router/
└── search/

knowledge/
├── runbooks/
├── services/
├── kubernetes/
├── imported/
├── confluence/
└── git/

catalog/
├── index.json
└── relationship_graph.json

docs/

scripts/
```

---

# Knowledge Lifecycle

## Filesystem

```text
Markdown Document
        ↓
OKF Validation
        ↓
Catalog
```

## Confluence

```text
Confluence Page
        ↓
Connector
        ↓
Raw Markdown Export
        ↓
OKF Conversion
        ↓
Validation
        ↓
Catalog
```

## Git

```text
Git Repository
        ↓
Document Discovery
        ↓
Raw Import
        ↓
OKF Conversion
        ↓
Validation
        ↓
Catalog
```

## Generated Intelligence

```text
Catalog
   ↓
Governance
   ↓
Service Catalog
   ↓
Relationship Graph
   ↓
Recommendations
   ↓
Context and Evidence
```

---

# Setup

## Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Configure Connector Variables

Example for Confluence:

```bash
export CONFLUENCE_USERNAME="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_PAGE_ID="your-page-id"
export CONFLUENCE_SPACE_KEY="your-space-key"
```

Do not commit credentials to source control.

## Configure Ollama

```bash
export OLLAMA_HOST="http://your-ollama-host:11434"
export OLLAMA_MODEL="phi3:mini"
```

---

# Core Commands

## Run Main Assistant Flow

```bash
python main.py
```

## Platform Sync

```bash
python scripts/platform_sync.py
```

## Test Confluence Connectivity

```bash
python scripts/test_confluence.py
```

## Import One Confluence Page

```bash
python scripts/import_confluence_page.py
```

## Import a Confluence Space

```bash
python scripts/import_confluence_space.py
```

## Import a Git Repository

```bash
python scripts/import_git_repo.py
```

## Knowledge Governance Report

```bash
python scripts/knowledge_report.py
```

## Service Overview

```bash
python scripts/service_overview.py
```

## Build Relationship Graph

```bash
python scripts/build_graph.py
```

## Relationship Graph Report

```bash
python scripts/relationship_graph_report.py
```

## Recommendation Report

```bash
python scripts/recommendation_report.py
```

## Context Package Test

```bash
python scripts/context_report.py
```

## Dashboard

```bash
python scripts/dashboard.py
```

## Query Knowledge

```bash
python scripts/query.py
```

---

# Recommended Operating Sequence

For a standard refresh and validation cycle:

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
python scripts/knowledge_report.py
python scripts/dashboard.py
python scripts/query.py
```

Run Confluence or Git import commands before platform synchronization when source content has changed.

---

# Current Capability Status

## Completed and Validated

### Platform Foundation

- OKF Standard
- Validation
- Catalog Generation

### Knowledge Sources

- Filesystem Connector
- Confluence Connector
- Git Connector

### Discovery

- Keyword Search
- Metadata Search
- Content Search
- Search Ranking
- Query Routing
- Document Retrieval

### Knowledge Management

- Governance V2
- Quality Scoring
- Duplicate Detection
- Service Catalog V2

### Knowledge Intelligence

- Relationship Graph V2
- Recommendation Engine
- Context Builder

### Platform Operations

- Platform Service
- Dashboard

### Traceable Retrieval

- Evidence Package
- Citation Builder
- Source Attribution
- Retrieval Trace
- Query Interface
- Hybrid Retrieval using keyword/content search and graph expansion

### Documentation

- Root README
- Architecture Guide
- Data Flow
- Deployment Guide
- User Guide
- Testing Guide
- Troubleshooting Guide
- Roadmap
- Changelog
- Module READMEs

## Implemented but Environment-Dependent

### Ollama Integration

- Remote endpoint configuration
- Generation request implementation
- Prompt integration
- Earlier grounded-response test

End-to-end Ollama generation remains environment-dependent because remote inference can time out.

## Partially Completed or Not Release-Validated

### Explainable RAG Generation

Completed foundations:

- Evidence Package
- Citation Builder
- Source Attribution
- Retrieval Trace

Pending validation:

- Generated answer plus evidence through the stable final query path

### ChromaDB and Semantic Retrieval

Pending validation or implementation:

- ChromaDB persistence test
- Vector index population test
- SemanticRetriever implementation
- Semantic query validation
- Vector-based hybrid ranking

---

# Release Validation Summary

The following release checks passed:

- Catalog generation
- Governance report
- Service Catalog
- Relationship Graph generation
- Relationship Graph report
- Recommendation foundation
- Context Builder
- Dashboard integration
- Query interface
- Source attribution
- Retrieval traceability
- Documentation coverage

Validated figures from the current test knowledge set:

```text
Documents: 13
Quality Score: 100.0%
Services: 12
Graph Nodes: 13
Relationships: 14
Recommendation Paths: 14
Platform Health: HEALTHY
```

---

# Known Limitations

- Semantic vector retrieval is not enabled in the validated query path.
- `SemanticRetriever` has not yet been implemented.
- ChromaDB persistence and vector counts have not been release-tested.
- `Vector Matches` is expected to be `0` in the current query output.
- Service names are inferred from document titles.
- Confluence space enumeration depends on API permissions and valid space keys.
- Remote Ollama inference can time out depending on environment and model performance.
- There is no REST API.
- There is no web UI.
- There is no authentication or document-level authorization.
- Synchronization is not yet scheduled or automated as a background service.

---

# Roadmap

## Completed

- Knowledge ingestion
- OKF validation
- Catalog generation
- Search and retrieval
- Governance
- Service Catalog
- Relationship Graph
- Recommendation Engine
- Context Builder
- Dashboard
- Platform Service
- Evidence Package
- Citation Builder
- Traceable query interface
- Hybrid retrieval using keyword/content search and graph expansion
- Documentation suite

## Next Priority

### Semantic Retrieval

- Implement `SemanticRetriever`
- Validate ChromaDB persistence
- Build and validate the vector index
- Test semantic queries that do not use exact document wording
- Merge keyword, vector, and graph scores

### Explainable RAG

- Build the final grounding prompt from the Evidence Package
- Generate a natural-language answer through Ollama
- Return answer, sources, related knowledge, and retrieval trace together
- Add deterministic fallback when Ollama is unavailable

## Productization

- FastAPI service
- Web UI
- Authentication and authorization
- Scheduled connector synchronization
- Background indexing
- Monitoring and structured logging
- Container deployment
- Kubernetes deployment

## Knowledge Model Improvements

- Explicit `service` metadata
- Typed graph relationships
- Service dependencies
- Knowledge review dates
- Stale-document detection
- Source-specific imported directories to avoid filename collisions

---

# Testing

The complete release validation procedure is documented in:

```text
docs/testing.md
```

Primary regression sequence:

```bash
python -m compileall app scripts
python scripts/platform_sync.py
python scripts/knowledge_report.py
python scripts/service_overview.py
python scripts/build_graph.py
python scripts/relationship_graph_report.py
python scripts/recommendation_report.py
python scripts/context_report.py
python scripts/dashboard.py
python scripts/query.py
```

---

# Troubleshooting

See:

```text
docs/troubleshooting.md
```

Common recovery sequence:

```bash
python scripts/platform_sync.py
python scripts/build_graph.py
python scripts/dashboard.py
python scripts/query.py
```

---

# Vision

OKF-IngestRAG aims to create a governed enterprise knowledge platform where:

```text
Knowledge Sources
       ↓
Governed Knowledge
       ↓
Connected Knowledge
       ↓
Explainable Retrieval
       ↓
AI-Ready Context
       ↓
Trusted Enterprise AI
```

The platform prioritizes knowledge quality, governance, traceability, and explainability. Semantic retrieval and LLM generation extend the platform only after the evidence and knowledge layers are reliable.
