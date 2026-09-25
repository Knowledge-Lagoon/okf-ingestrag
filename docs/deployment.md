# Deployment Guide

OKF-IngestRAG Deployment and Operational Guide

---

# Overview

This document describes how to deploy, configure, initialize, and operate the OKF-IngestRAG platform.

The current deployment model is intended for:

- Development environments
- Proof of Concept deployments
- Internal platform testing
- Local and VM-hosted environments

The platform currently supports:

```text
Filesystem Knowledge
Confluence Knowledge
Git Knowledge

Catalog
Governance
Service Catalog
Relationship Graph

Vector Search
Hybrid Retrieval

Dashboard
Assistant
```

---

# Deployment Architecture

```text
Knowledge Sources

Filesystem
Confluence
Git

       ↓

OKF Platform

       ↓

Catalog

       ↓

Relationship Graph

       ↓

Vector Index

       ↓

Hybrid Retrieval

       ↓

Assistant
```

---

# System Requirements

## Minimum

```text
CPU: 2 Core

Memory: 4 GB

Disk: 10 GB

Python: 3.10+
```

---

## Recommended

```text
CPU: 4+ Core

Memory: 8 GB+

Disk: 20+ GB

Python: 3.11+
```

---

# Repository Setup

Clone the repository:

```bash
git clone <repository-url>

cd okf-ingestrag
```

---

# Python Environment

Create a virtual environment:

```bash
python -m venv venv
```

---

## Linux

Activate:

```bash
source venv/bin/activate
```

---

## macOS

Activate:

```bash
source venv/bin/activate
```

---

## Windows

Activate:

```powershell
venv\Scripts\activate
```

---

# Install Dependencies

Install project packages:

```bash
pip install -r requirements.txt
```

Verify:

```bash
pip list
```

---

# Environment Variables

Create:

```text
.env
```

Example:

```bash
CONFLUENCE_URL=https://your-company.atlassian.net

CONFLUENCE_USERNAME=user@example.com

CONFLUENCE_API_TOKEN=xxxxxxxx

OLLAMA_HOST=http://172.31.15.13:11434

OLLAMA_MODEL=llama3

OLLAMA_EMBEDDING_MODEL=all-minilm
```

---

# Repository Structure

```text
app/
catalog/
data/
docs/
knowledge/
scripts/
```

---

# Initial Knowledge Layout

```text
knowledge/

├── runbooks/
├── services/
├── kubernetes/

├── imported/
├── confluence/
└── git/
```

---

# First-Time Initialization

## Step 1

Validate local knowledge documents.

```bash
python main.py
```

Expected:

```text
Catalog Generated

Search Ready
```

---

## Step 2

Run platform synchronization.

```bash
python scripts/platform_sync.py
```

This performs:

```text
Catalog Refresh

Governance

Service Catalog

Relationship Graph
```

---

## Step 3

Build relationship graph.

```bash
python scripts/build_graph.py
```

Artifact:

```text
catalog/relationship_graph.json
```

---

# Confluence Import

## Import Single Page

```bash
python scripts/import_confluence_page.py
```

---

## Import Space

```bash
python scripts/import_confluence_space.py
```

This imports documentation into:

```text
knowledge/confluence/
```

and converts to OKF documents.

---

# Git Import

Import documentation from a repository.

```bash
python scripts/import_git_repo.py
```

Imported content:

```text
README.md

Runbooks

Documentation
```

---

# Catalog Generation

Artifact:

```text
catalog/index.json
```

Contains:

```text
Metadata

Document Type

Content

Ownership

Source Information
```

This is regenerated during platform synchronization.

---

# Service Catalog

Generate service relationships.

```bash
python scripts/service_overview.py
```

Example output:

```text
Service: Kong

Runbooks
Documentation
Owners
Sources
```

---

# Governance

Generate governance report.

```bash
python scripts/knowledge_report.py
```

Provides:

```text
Knowledge Quality

Missing Owners

Missing Tags

Duplicate Titles
```

---

# Dashboard

Generate platform dashboard.

```bash
python scripts/dashboard.py
```

Expected:

```text
Total Documents

Services

Relationships

Quality Score

Platform Health
```

---

# Relationship Graph

Build graph:

```bash
python scripts/build_graph.py
```

Artifact:

```text
catalog/relationship_graph.json
```

View:

```bash
python scripts/relationship_graph_report.py
```

---

# Recommendation Engine

Run:

```bash
python scripts/recommendation_report.py
```

Output:

```text
Primary Document

Suggested Knowledge

Relationship Scores
```

---

# Vector Database Setup

The platform uses:

```text
ChromaDB
```

for semantic retrieval.

Storage:

```text
data/chroma/
```

---

# Build Vector Index

Generate embeddings and create vector index:

```bash
python scripts/build_vector_index.py
```

Expected:

```text
Documents processed

Chunks indexed

Vector store count
```

---

# Semantic Search

Test vector search:

```bash
python scripts/test_semantic_search.py
```

Example:

```text
Why are my pods restarting?
```

Expected results:

```text
CrashLoopBackOff

ImagePullBackOff

Kubernetes Troubleshooting
```

---

# Hybrid Retrieval

The platform supports:

```text
Keyword Search

+

Vector Search

+

Relationship Graph
```

through the Hybrid Retriever.

---

# Query Interface

Run:

```bash
python scripts/query.py
```

Example:

```text
Ask a question:
```

Input:

```text
Why are my pods restarting?
```

Output:

```text
Sources

Related Knowledge

Retrieval Trace
```

---

# Ollama Integration

The platform is designed to work with a remote Ollama instance.

Verify connectivity:

```bash
curl http://HOST:11434/api/tags
```

Expected:

```json
{
  "models": [...]
}
```

---

## Generate Embeddings

Verify embedding model:

```bash
curl http://HOST:11434/api/embed
```

---

# Operational Workflow

Recommended workflow:

```bash
python scripts/platform_sync.py

python scripts/build_graph.py

python scripts/build_vector_index.py

python scripts/dashboard.py
```

---

# Platform Refresh Workflow

Daily refresh sequence:

```text
Confluence Import

↓

Git Import

↓

Catalog Refresh

↓

Graph Refresh

↓

Vector Refresh

↓

Dashboard
```

---

# Backup Strategy

Persist these directories:

```text
catalog/

knowledge/

data/chroma/
```

Recommended:

```bash
tar -czf backup.tar.gz \
catalog \
knowledge \
data/chroma
```

---

# Troubleshooting

## Catalog Missing

Check:

```text
catalog/index.json
```

Rebuild:

```bash
python scripts/platform_sync.py
```

---

## Relationship Graph Missing

Check:

```text
catalog/relationship_graph.json
```

Rebuild:

```bash
python scripts/build_graph.py
```

---

## No Semantic Results

Verify:

```bash
python scripts/build_vector_index.py
```

Check:

```text
data/chroma/
```

exists.

---

## Ollama Connection Failure

Verify:

```bash
curl http://HOST:11434/api/tags
```

Check:

```text
OLLAMA_HOST
```

environment variable.

---

## Confluence Authentication Failure

Verify:

```text
CONFLUENCE_URL

CONFLUENCE_USERNAME

CONFLUENCE_API_TOKEN
```

---

## Empty Dashboard

Verify:

```text
catalog/index.json
```

contains documents.

Run:

```bash
python scripts/platform_sync.py
```

again.

---

# Release Checklist

Before releasing:

```text
✅ Platform Sync Successful

✅ Governance Report Successful

✅ Dashboard Generated

✅ Relationship Graph Generated

✅ Vector Index Created

✅ Semantic Search Working

✅ Query Interface Working

✅ Documentation Complete
```

---

# Current Deployment Model

Version 1.1 deployment supports:

```text
Local Development

VM-Based Deployment

Internal POC Deployment
```

Future versions may support:

```text
Docker

Kubernetes

FastAPI

Web UI

Authentication
```

---

# Summary

Deploying OKF-IngestRAG consists of:

```text
Install

↓

Configure

↓

Import Knowledge

↓

Build Catalog

↓

Build Graph

↓

Build Vector Index

↓

Run Dashboard

↓

Query Knowledge
```

The result is a governed, explainable, hybrid retrieval platform that combines structured OKF knowledge, semantic search, relationship mapping, and AI-ready context generation.