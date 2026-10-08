# OKF-IngestRAG Data Flow

Data Flow and Processing Architecture

---

# Purpose

This document explains how knowledge moves through the OKF-IngestRAG platform.

It covers:

- Knowledge ingestion
- OKF conversion
- Catalog generation
- Knowledge intelligence
- Search and retrieval
- Hybrid RAG
- Assistant response generation

---

# End-to-End Platform Flow

```text
Knowledge Sources
       ↓

OKF Conversion
       ↓

Validation
       ↓

Catalog
       ↓

Knowledge Intelligence
       ↓

Search and Retrieval
       ↓

Context Assembly
       ↓

Evidence Package
       ↓

Assistant
       ↓

Optional LLM
       ↓

Answer
```

---

# Flow 1 - Knowledge Ingestion

## Filesystem

```text
Markdown Files
        ↓
OKF Validator
        ↓
Catalog
```

Example:

```text
knowledge/runbooks/kong-restart.md
```

---

## Confluence

```text
Confluence Page
        ↓
Connector
        ↓
Markdown Export
        ↓
OKF Conversion
        ↓
Validation
        ↓
Catalog
```

Generated content:

```text
knowledge/imported/
```

---

## Git

```text
Git Repository
        ↓
Clone
        ↓
Document Discovery
        ↓
OKF Conversion
        ↓
Validation
        ↓
Catalog
```

---

# Flow 2 - Catalog Generation

All valid OKF documents are transformed into:

```text
catalog/index.json
```

---

## Input

```text
knowledge/runbooks/

knowledge/services/

knowledge/imported/
```

---

## Processing

Extract:

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

---

## Output

```json
{
  "title": "Kong Restart",
  "type": "runbook",
  "owner": "devops"
}
```

---

# Flow 3 - Governance

Catalog becomes input for governance analysis.

```text
Catalog
      ↓
Governance Analyzer
      ↓
Knowledge Metrics
```

---

## Outputs

```text
Quality Score

Missing Owners

Missing Tags

Missing Descriptions

Duplicates
```

---

# Flow 4 - Service Catalog

Catalog entries are grouped into services.

```text
Catalog
      ↓
Service Catalog
      ↓
Service View
```

---

## Example

```text
Kong Restart
Kong API Gateway
```

becomes

```text
Service: Kong
```

---

## Output

```json
{
  "kong": {
      "runbooks": [],
      "documentation": []
  }
}
```

---

# Flow 5 - Relationship Graph

Catalog metadata generates relationships.

```text
Catalog
       ↓

Tag Analysis
       ↓

Relationship Graph
```

---

## Example

Document:

```text
Kong Restart

tags:
- kong
- kubernetes
```

Document:

```text
Kong API Gateway

tags:
- kong
- kubernetes
```

Generated relationship:

```text
Kong Restart
      |
      +--- Kong API Gateway
```

---

## Output

```text
catalog/relationship_graph.json
```

---

# Flow 6 - Recommendation Engine

Recommendations use graph relationships.

```text
Relationship Graph
        ↓
Recommendation Engine
        ↓
Suggested Knowledge
```

---

Example:

```text
Primary:
Kong Restart

Recommended:
Kong API Gateway
```

---

# Flow 7 - Dashboard

Dashboard aggregates platform metrics.

```text
Catalog
     +
Governance
     +
Service Catalog
     +
Relationship Graph

     ↓

Dashboard
```

Output:

```text
Documents

Services

Relationships

Quality Score
```

---

# Flow 8 - Traditional Search

Keyword-based retrieval.

```text
Question
      ↓

Search Engine

      ↓

Matching Documents
```

---

Question:

```text
Kong Restart
```

Result:

```text
Kong Restart
```

---

# Flow 9 - Semantic Retrieval

Vector-based retrieval.

```text
Question
       ↓

Chunk Query
       ↓

Embedding
       ↓

Vector Search
       ↓

Relevant Chunks
```

---

Question:

```text
Why do my pods keep restarting?
```

Result:

```text
CrashLoopBackOff
```

even if exact wording does not exist.

---

# Flow 10 - Vector Index Generation

Knowledge content is indexed for semantic search.

```text
Catalog
      ↓

Chunking

      ↓

Embeddings

      ↓

ChromaDB
```

---

## Chunking

Example:

```text
1200 length chunks

200 overlap
```

---

## Embeddings

Generated using:

```text
Ollama

embeddinggemma

or

all-minilm
```

---

## Output

```text
data/chroma/
```

---

# Flow 11 - Hybrid Retrieval

Hybrid Retrieval combines multiple retrieval mechanisms.

```text
Question
      ↓

Keyword Search

      +
      +

Semantic Search

      +
      +

Graph Expansion

      ↓

Evidence Package
```

---

# Retrieval Sources

## Keyword Search

Provides:

```text
Exact Matches

Metadata Matches
```

---

## Semantic Search

Provides:

```text
Concept Matches

Natural Language Matches
```

---

## Graph Expansion

Provides:

```text
Related Knowledge

Recommendations
```

---

# Flow 12 - Context Builder

All retrieved information is assembled into a context package.

```text
Primary Document

       +

Service Information

       +

Related Knowledge

       +

Recommendations

       ↓

Context Package
```

---

## Example

```json
{
  "primary_document":
      "Kong Restart",

  "related_documents":
      [
          "Kong API Gateway"
      ]
}
```

---

# Flow 13 - Evidence Package

Evidence Package becomes the trust layer.

```text
Hybrid Retrieval
         ↓

Evidence Package
         ↓

Citations
```

---

## Contents

```text
Question

Keyword Matches

Vector Matches

Graph Matches

Recommendations
```

---

# Flow 14 - Citation Builder

Produces source references.

```text
Evidence Package
         ↓
Citation Builder
         ↓
Sources
```

---

Example:

```text
CrashLoopBackOff

knowledge/imported/crashloopbackoff.md
```

---

# Flow 15 - Assistant

Assistant converts evidence into user-facing output.

```text
Evidence Package
         ↓

Assistant
         ↓

Formatted Response
```

---

Output includes:

```text
Answer

Sources

Related Knowledge

Retrieval Trace
```

---

# Flow 16 - Optional LLM

LLM consumes evidence package.

```text
Evidence Package
         ↓

Prompt Builder
         ↓

LLM
         ↓

Generated Answer
```

---

Important:

```text
LLM never bypasses evidence.
```

---

# Hybrid RAG Flow

Complete AI flow:

```text
Question
      ↓

Keyword Search

      +

Vector Search

      +

Relationship Graph

      ↓

Evidence Package

      ↓

Citation Builder

      ↓

Context Builder

      ↓

LLM

      ↓

Answer

      +

Sources

      +

Traceability
```

---

# Platform Refresh Flow

```text
Confluence
      ↓

Git
      ↓

Filesystem
      ↓

Catalog
      ↓

Governance
      ↓

Service Catalog
      ↓

Relationship Graph
      ↓

Vector Index
      ↓

Dashboard
```

---

# Recovery Flow

When platform state becomes invalid:

```text
Catalog
      ↓

Graph
      ↓

Vector Index
      ↓

Dashboard
      ↓

Query Validation
```

Execute:

```bash
python scripts/platform_sync.py

python scripts/build_graph.py

python scripts/build_vector_index.py

python scripts/dashboard.py

python scripts/query.py
```

---

# Source of Truth Hierarchy

The platform treats data sources as follows:

```text
1. OKF Documents

2. Catalog

3. Relationship Graph

4. Vector Index

5. Context Packages

6. Generated Responses
```

Important:

```text
Generated responses
are never the source of truth.
```

---

# Summary

OKF-IngestRAG processes enterprise knowledge through a structured lifecycle:

```text
Ingest
   ↓

Validate
   ↓

Catalog
   ↓

Connect
   ↓

Search
   ↓

Retrieve
   ↓

Explain
   ↓

Generate
```

The result is a governed, explainable, service-aware, hybrid retrieval platform capable of supporting enterprise RAG and future agentic AI workloads.