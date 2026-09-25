# OKF-IngestRAG Architecture

Enterprise Knowledge Ingestion, Governance, Discovery, and Hybrid RAG Platform

---

# Overview

OKF-IngestRAG is a knowledge platform designed to transform distributed enterprise knowledge into a governed, searchable, explainable, and AI-ready knowledge ecosystem.

The platform combines:

- Structured knowledge (OKF)
- Governance
- Service awareness
- Relationship mapping
- Recommendation generation
- Hybrid retrieval
- Explainable RAG

Unlike traditional RAG architectures that rely primarily on vector databases, OKF-IngestRAG treats knowledge as a governed asset before it becomes AI context.

---

# Architecture Principles

The platform follows six key principles:

## 1. Knowledge First

Knowledge must be curated before it is consumed by AI.

```text
Knowledge
    ↓
Governance
    ↓
Discovery
    ↓
AI
```

---

## 2. Explainability

Every answer should be traceable back to its source.

```text
Answer
+
Sources
+
Retrieval Trace
```

---

## 3. Hybrid Retrieval

Keyword search and semantic search work together.

```text
OKF Search
+
Vector Search
+
Relationship Graph
```

---

## 4. Service Awareness

Knowledge should be organized around services rather than isolated documents.

---

## 5. Relationship Awareness

Related knowledge should be discoverable automatically.

---

## 6. AI Optional

The platform remains useful even without an LLM.

---

# High-Level Architecture

```text
Knowledge Sources
=================

Filesystem
Confluence
Git

        ↓

Open Knowledge Format (OKF)

        ↓

Validation

        ↓

Catalog

        ↓

Knowledge Intelligence Layer

    Governance
    Service Catalog
    Relationship Graph
    Recommendations

        ↓

Discovery Layer

    Search
    Ranking
    Routing
    Retrieval

        ↓

Hybrid Retrieval

    Keyword Search
    Semantic Search
    Graph Expansion

        ↓

Context Builder

        ↓

Evidence Package

        ↓

Assistant

        ↓

Optional LLM
```

---

# Layer 1 - Knowledge Sources

The platform currently supports three knowledge sources.

## Filesystem

Local Markdown-based documentation.

Examples:

```text
Runbooks
Operational Procedures
Service Documentation
```

Location:

```text
knowledge/
```

---

## Confluence

Enterprise documentation platform.

Supported capabilities:

```text
Single Page Import
Bulk Space Import
Markdown Export
OKF Conversion
```

---

## Git

Documentation and knowledge maintained in source control.

Supported content:

```text
README.md
Architecture Guides
Runbooks
Operational Notes
```

---

# Layer 2 - Open Knowledge Format (OKF)

All knowledge is normalized into a standard format.

Example:

```yaml
---
title: Kong Restart
type: runbook
owner: devops
source: confluence
version: 1.0
tags:
  - kong
  - kubernetes
---
```

Benefits:

```text
Consistency
Governance
Traceability
Searchability
AI Readiness
```

---

# Layer 3 - Validation

The validation layer verifies:

```text
YAML Frontmatter
Required Metadata
Document Structure
```

Invalid documents are excluded from the catalog.

---

# Layer 4 - Catalog

The catalog is the central inventory of valid knowledge.

Generated artifact:

```text
catalog/index.json
```

Contents:

```text
Title
Type
Description
Owner
Source
Tags
Path
Content
```

The catalog acts as the platform's primary search index.

---

# Layer 5 - Knowledge Intelligence

This layer adds meaning to the catalog.

---

## Governance

Evaluates knowledge quality.

Metrics:

```text
Total Documents
Documents by Type
Documents by Source
Missing Owners
Missing Tags
Missing Descriptions
Duplicate Titles
Quality Score
```

---

## Service Catalog

Groups documents into services.

Example:

```text
Kong

├── Runbooks
├── Documentation
├── Sources
├── Owners
└── Tags
```

Current service identification:

```text
First word of the title
```

Future version:

```yaml
service: kong
```

---

## Relationship Graph

Identifies related knowledge using metadata.

Current relationship rule:

```text
Shared Tags
```

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

---

## Recommendation Engine

Suggests additional knowledge.

Example:

```text
Primary:
Kong Restart

Recommended:
Kong API Gateway
CrashLoopBackOff
```

Recommendations are based on graph relationships.

---

# Layer 6 - Discovery

Discovery is responsible for locating relevant knowledge.

Components:

```text
Search
Ranking
Routing
Retrieval
```

---

## Search

Provides:

```text
Keyword Matching
Metadata Matching
Content Matching
```

---

## Ranking

Orders search results according to relevance.

---

## Query Routing

Identifies the most suitable retrieval path.

Examples:

```text
Service Question
Runbook Question
General Knowledge Question
```

---

## Retrieval

Loads content from matching knowledge documents.

---

# Layer 7 - Hybrid Retrieval

Hybrid Retrieval combines:

```text
Keyword Search
+
Semantic Search
+
Graph Expansion
```

This is the foundation of the platform's RAG strategy.

---

## Traditional Search

Best for:

```text
Exact Terms
Runbooks
Service Names
Tags
```

Example:

```text
Kong Restart
```

---

## Semantic Search

Best for:

```text
Natural Language Questions
Concept Matching
Related Terms
```

Example:

```text
Why do my pods restart?
```

May find:

```text
CrashLoopBackOff
```

without exact keyword matches.

---

## Graph Expansion

Retrieves related knowledge.

Example:

```text
CrashLoopBackOff

     ↓

ImagePullBackOff
Kubernetes Troubleshooting
```

---

# Layer 8 - Vector Database

The vector layer supports semantic retrieval.

---

## Chunking

Documents are broken into chunks.

Example:

```text
1200 characters

200 character overlap
```

---

## Embeddings

Chunks are converted into vectors.

Planned model:

```text
Ollama all-minilm
```

or:

```text
embeddinggemma
```

---

## Vector Store

Planned implementation:

```text
ChromaDB
```

Storage location:

```text
data/chroma/
```

---

# Layer 9 - Context Builder

The Context Builder assembles information from multiple platform components.

Inputs:

```text
Primary Document
Related Documents
Service Information
Recommendations
```

Output:

```json
{
  "query": "...",
  "primary_document": "...",
  "related_documents": []
}
```

---

# Layer 10 - Evidence Layer

The Evidence Layer provides traceability.

Components:

```text
Evidence Package
Citation Builder
```

Purpose:

```text
Answer
+
Sources
+
Traceability
```

---

## Evidence Package

Contains:

```text
Question
Keyword Matches
Vector Matches
Graph Matches
Recommendations
```

---

## Citation Builder

Produces:

```text
Source References
Document Paths
Ownership Information
```

---

# Layer 11 - Assistant

The Assistant converts retrieved evidence into human-readable output.

Responsibilities:

```text
Response Formatting
Source Presentation
Retrieval Trace
Recommendations
```

The Assistant does not perform retrieval.

---

# Layer 12 - Optional LLM

An LLM may consume evidence packages.

Examples:

```text
Ollama
OpenAI
Azure OpenAI
```

Planned flow:

```text
Evidence Package
        ↓
LLM
        ↓
Answer
```

The LLM should never bypass the evidence layer.

---

# RAG Architecture

The platform implements Explainable Hybrid RAG.

```text
Question
     ↓

Hybrid Retriever

 ├─ Keyword Search
 ├─ Vector Search
 ├─ Graph Expansion

     ↓

Evidence Package

     ↓

Citations

     ↓

LLM

     ↓

Answer + Sources
```

---

# Example End-to-End Flow

Question:

```text
Why are my pods restarting?
```

---

Search:

```text
CrashLoopBackOff
```

---

Vector Search:

```text
Kubernetes Pod Troubleshooting
```

---

Graph Expansion:

```text
ImagePullBackOff
```

---

Evidence Package:

```text
Keyword Matches: 1

Vector Matches: 2

Graph Matches: 1
```

---

Assistant Output:

```text
Answer

Sources:
- CrashLoopBackOff
- Kubernetes Troubleshooting

Related Knowledge:
- ImagePullBackOff

Retrieval Trace:
Keyword: 1
Vector: 2
Graph: 1
```

---

# Operational Components

## Platform Service

Provides orchestration.

Responsibilities:

```text
Catalog Refresh
Governance
Service Catalog
Relationship Graph
```

---

## Dashboard

Provides operational visibility.

Metrics:

```text
Documents
Sources
Quality Score
Services
Relationships
Recommendations
```

---

# Repository Architecture

```text
app/
├── assistant/
├── catalog/
├── connectors/
├── context/
├── dashboard/
├── embeddings/
├── governance/
├── graph/
├── platform/
├── rag/
├── recommendations/
├── retrieval/
├── router/
├── search/
└── vector/

catalog/

knowledge/

scripts/

docs/
```

---

# Current State

## Completed

```text
Knowledge Sources
OKF
Validation
Catalog
Search
Governance
Service Catalog
Relationship Graph
Recommendations
Context Builder
Dashboard
Platform Service
```

## In Progress

```text
Vector Database
Semantic Search
Hybrid Retrieval
Explainable RAG
```

## Future

```text
FastAPI
Web UI
Authentication
Scheduling
Deployment Automation
```

---

# Vision

The goal of OKF-IngestRAG is to create an enterprise knowledge platform where:

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

The platform prioritizes governance, explainability, and traceability before AI generation.