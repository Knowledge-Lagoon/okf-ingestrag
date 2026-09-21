# OKF-IngestRAG

Enterprise Knowledge Ingestion, Governance, Discovery and AI Context Platform

---

## Overview

OKF-IngestRAG is an enterprise knowledge platform that ingests knowledge from multiple sources, converts it into the Open Knowledge Format (OKF), validates and indexes content, and builds governance, service awareness, relationship mapping, and AI-ready context packages.

The platform is designed to support operational knowledge, runbooks, service documentation, architecture guidance, and AI-assisted knowledge retrieval.

Unlike traditional RAG implementations that focus primarily on embeddings and vector databases, OKF-IngestRAG focuses on structured, governed, traceable knowledge before introducing AI.

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

### Open Knowledge Format (OKF)

All ingested content is converted into a standard OKF structure.

Benefits:

- Consistent metadata
- Traceability
- Source attribution
- Searchability
- Governance
- AI readiness

### AI Ready by Design

The platform creates context packages that can be consumed by:

- Local LLMs
- Ollama
- Agent frameworks
- Future RAG solutions

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

- Page retrieval
- Content extraction
- Bulk space import
- Automatic OKF conversion

### Git Repositories

Supports:

- README files
- Documentation
- Runbooks
- Architecture guides

---

## Knowledge Processing

### OKF Conversion

Converts imported content into standard OKF documents.

Example:

```yaml
---
type: runbook
title: Kong Restart
owner: devops
source: confluence
version: 1.0
---
```

### Validation

Checks:

- YAML frontmatter
- Required fields
- Metadata structure

### Catalog Generation

Generates:

```text
catalog/index.json
```

The catalog serves as the searchable inventory of all valid knowledge.

---

## Knowledge Discovery

### Search

Supports:

- Metadata matching
- Content matching
- Ranked results

### Query Routing

Routes questions to:

- Runbooks
- Services
- General knowledge

### Retrieval

Loads relevant content from matching documents.

---

## Knowledge Governance

Governance V2 provides:

### Knowledge Health Metrics

- Total Documents
- Documents By Type
- Documents By Source

### Quality Validation

- Missing Owners
- Missing Tags
- Missing Descriptions

### Duplicate Detection

Identifies duplicate titles and overlapping knowledge.

### Quality Score

Provides a platform-level knowledge quality score.

---

## Service Catalog

The Service Catalog groups knowledge by service.

Example:

```text
Kong

├── Runbooks
├── Documentation
├── Owners
├── Sources
└── Tags
```

This allows service-oriented navigation through the knowledge estate.

---

## Relationship Graph

The Relationship Graph identifies relationships between documents.

Relationships are currently created from shared tags.

Example:

```text
Kong Restart
      │
      └── Kong API Gateway
```

Produces:

```text
catalog/relationship_graph.json
```

Future versions will support:

- Relationship scoring
- Dependency mapping
- Service impact analysis

---

## Context Builder

The Context Builder creates structured knowledge packages.

Example:

```json
{
  "query": "Tell me about Kong",
  "primary_document": "Kong API Gateway",
  "related_documents": [
    "Kong Restart"
  ]
}
```

These context packages are designed for AI consumption.

---

## Assistant

Assistant V2 provides:

- Structured responses
- Source attribution
- Service awareness
- Related knowledge recommendations

The assistant can operate:

- Without an LLM
- With a local Ollama deployment
- With future AI providers

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

        ↓

Retrieval

        ↓

Service Catalog
Relationship Graph

        ↓

Context Builder

        ↓

Assistant

        ↓

LLM
```

---

# Repository Structure

```text
app/
├── assistant/
├── catalog/
├── connectors/
├── context/
├── governance/
├── graph/
├── llm/
├── okf/
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

scripts/
```

---

# Knowledge Lifecycle

## Confluence

```text
Confluence
     ↓
Import
     ↓
Markdown Export
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
OKF Conversion
      ↓
Validation
      ↓
Catalog
```

## Filesystem

```text
Markdown Documents
       ↓
Validation
       ↓
Catalog
```

---

# Core Commands

## Run Assistant

```bash
python main.py
```

---

## Import Confluence Page

```bash
python scripts/import_confluence_page.py
```

---

## Import Confluence Space

```bash
python scripts/import_confluence_space.py
```

---

## Import Git Repository

```bash
python scripts/import_git_repo.py
```

---

## Knowledge Governance Report

```bash
python scripts/knowledge_report.py
```

---

## Service Overview

```bash
python scripts/service_overview.py
```

---

## Build Relationship Graph

```bash
python scripts/build_graph.py
```

---

## Relationship Graph Report

```bash
python scripts/relationship_graph_report.py
```

---

## Context Package Test

```bash
python scripts/context_report.py
```

---

## Platform Sync

```bash
python scripts/sync_all.py
```

---

# Current Status

## Completed

### Platform Foundation

- OKF Standard
- Validation
- Catalog Generation

### Knowledge Sources

- Filesystem
- Confluence
- Git

### Discovery

- Search
- Ranking
- Routing
- Retrieval

### Knowledge Management

- Governance V2
- Service Catalog V2

### Knowledge Intelligence

- Relationship Graph V2
- Context Builder

### Assistant

- Assistant V2

---

# Roadmap

## Phase 1 ✅

Knowledge Ingestion

## Phase 2 ✅

Search and Retrieval

## Phase 3 ✅

Governance

## Phase 4 ✅

Service Catalog

## Phase 5 ✅

Relationship Graph

## Phase 6 ✅

Context Builder

## Phase 7

Enhanced Assistant

### Planned

- Rich Service Views
- Relationship Scoring
- Knowledge Dashboard
- Automated Synchronization
- Context Export

## Phase 8

AI Context Engine

### Planned

- Ollama Integration Stabilization
- Context-to-LLM Pipelines
- Graph-Assisted Retrieval
- Hybrid Search

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

AI Ready Context

       ↓

Reliable Enterprise AI
```

The platform emphasizes knowledge quality, traceability, governance, and explainability before introducing advanced AI capabilities.