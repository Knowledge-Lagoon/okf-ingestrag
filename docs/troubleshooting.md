# Troubleshooting Guide

OKF-IngestRAG Troubleshooting and Diagnostics

---

# Overview

This document provides troubleshooting guidance for the OKF-IngestRAG platform.

The guide covers:

- Catalog generation issues
- Confluence import issues
- Git import issues
- Governance issues
- Relationship graph problems
- Vector database issues
- Semantic search issues
- Dashboard issues
- Query and retrieval issues
- Ollama connectivity issues

---

# Troubleshooting Workflow

When diagnosing a problem, use the following order:

```text
1. Check Logs

2. Validate Source Content

3. Verify Catalog

4. Verify Graph

5. Verify Vector Index

6. Verify Retrieval

7. Verify Assistant
```

---

# General Diagnostics

## Verify Python Environment

Check Python version:

```bash
python --version
```

Expected:

```text
Python 3.10+
```

---

## Verify Dependencies

Check installed packages:

```bash
pip list
```

If dependencies are missing:

```bash
pip install -r requirements.txt
```

---

## Verify Project Structure

Confirm expected directories exist:

```bash
ls
```

Expected:

```text
app/
catalog/
knowledge/
scripts/
docs/
```

---

# Catalog Issues

---

## Problem

Catalog file missing.

Error:

```text
catalog/index.json not found
```

---

## Cause

Catalog has not been generated.

---

## Resolution

Run:

```bash
python scripts/platform_sync.py
```

or:

```bash
python main.py
```

Verify:

```bash
ls catalog
```

Expected:

```text
index.json
```

---

## Problem

Catalog is empty.

Example:

```json
[]
```

---

## Cause

No valid OKF documents found.

---

## Resolution

Verify documents contain valid frontmatter.

Example:

```yaml
---
title: Kong Restart
type: runbook
owner: devops
---
```

Then rebuild:

```bash
python scripts/platform_sync.py
```

---

# Validation Issues

---

## Problem

Document appears as invalid.

Example:

```text
Missing owner
Missing title
Invalid metadata
```

---

## Cause

Required fields are missing.

---

## Resolution

Verify frontmatter contains:

```yaml
title:
type:
owner:
source:
```

Retry:

```bash
python main.py
```

---

# Filesystem Knowledge Issues

---

## Problem

Knowledge files are not indexed.

---

## Cause

Files may be stored outside monitored directories.

---

## Resolution

Store knowledge in:

```text
knowledge/runbooks/

knowledge/services/

knowledge/kubernetes/

knowledge/imported/
```

Rebuild catalog.

---

# Confluence Issues

---

## Problem

Authentication failure.

Example:

```text
401 Unauthorized

403 Forbidden
```

---

## Cause

Invalid credentials or token.

---

## Resolution

Verify:

```bash
CONFLUENCE_URL

CONFLUENCE_USERNAME

CONFLUENCE_API_TOKEN
```

Check environment variables:

```bash
echo $CONFLUENCE_URL
```

---

## Problem

No pages imported.

---

## Cause

Incorrect page ID or space key.

---

## Resolution

Verify:

```text
Page ID

Space Key
```

Retry:

```bash
python scripts/import_confluence_page.py

python scripts/import_confluence_space.py
```

---

## Problem

Imported Confluence files appear invalid.

---

## Cause

Raw Confluence exports do not contain OKF metadata.

---

## Resolution

This is expected.

Raw imports:

```text
knowledge/confluence/
```

Converted OKF documents:

```text
knowledge/imported/
```

Only converted documents should be indexed.

---

# Git Import Issues

---

## Problem

No Git documents imported.

---

## Cause

Repository URL is incorrect or inaccessible.

---

## Resolution

Verify:

```bash
git clone <repository>
```

works manually.

Retry:

```bash
python scripts/import_git_repo.py
```

---

## Problem

README not appearing in catalog.

---

## Cause

OKF conversion may not have completed.

---

## Resolution

Re-run:

```bash
python scripts/import_git_repo.py

python scripts/platform_sync.py
```

---

# Governance Issues

---

## Problem

Quality score unexpectedly low.

---

## Cause

Missing metadata.

---

## Resolution

Run:

```bash
python scripts/knowledge_report.py
```

Review:

```text
Missing Owners

Missing Tags

Missing Descriptions
```

Complete missing metadata.

---

## Problem

Duplicate documents reported.

---

## Cause

Multiple documents use the same title.

---

## Resolution

Locate duplicates:

```bash
python scripts/knowledge_report.py
```

Rename duplicate documents.

---

# Service Catalog Issues

---

## Problem

Service grouping appears incorrect.

Example:

```text
Kong Restart

Kong Troubleshooting
```

not grouped together.

---

## Cause

Current implementation derives service names from titles.

---

## Resolution

Review title naming consistency.

Current MVP rule:

```text
First word of the title
```

---

# Relationship Graph Issues

---

## Problem

Relationship graph not generated.

---

## Resolution

Run:

```bash
python scripts/build_graph.py
```

Verify:

```bash
ls catalog
```

Expected:

```text
relationship_graph.json
```

---

## Problem

No relationships found.

---

## Cause

Documents do not share tags.

---

## Resolution

Verify metadata:

```yaml
tags:
  - kong
  - kubernetes
```

Shared tags are required for Relationship Graph V1.

---

## Problem

Unexpected relationships appear.

---

## Cause

Generic tags create noise.

Example:

```text
git
confluence
imported
```

---

## Resolution

Add ignored-tag filtering.

Suggested:

```python
IGNORED_TAGS = {
    "git",
    "confluence",
    "imported",
    "manual"
}
```

---

# Recommendation Issues

---

## Problem

No recommendations returned.

---

## Cause

Relationship graph contains no related documents.

---

## Resolution

Check graph:

```bash
python scripts/relationship_graph_report.py
```

Ensure relationships exist.

---

# Dashboard Issues

---

## Problem

Dashboard fails to load.

---

## Resolution

Verify:

```text
catalog/index.json

catalog/relationship_graph.json
```

exist.

Then rerun:

```bash
python scripts/platform_sync.py

python scripts/build_graph.py
```

---

## Problem

Dashboard shows zero relationships.

---

## Cause

Relationship graph not generated.

---

## Resolution

Rebuild graph:

```bash
python scripts/build_graph.py
```

---

# Vector Database Issues

---

## Problem

Vector store not created.

---

## Resolution

Verify directory:

```bash
ls data
```

Expected:

```text
chroma/
```

Rebuild:

```bash
python scripts/build_vector_index.py
```

---

## Problem

Vector count is zero.

---

## Cause

No chunks were indexed.

---

## Resolution

Verify:

```text
catalog/index.json
```

contains content.

Check:

```text
Document content is not empty.
```

Rebuild index.

---

# Semantic Search Issues

---

## Problem

No semantic search results returned.

---

## Cause

Embeddings not generated.

---

## Resolution

Rebuild vector index:

```bash
python scripts/build_vector_index.py
```

Verify:

```text
Vector store count > 0
```

---

## Problem

Poor search quality.

---

## Cause

Small knowledge base or weak embeddings.

---

## Resolution

Verify:

```text
Chunking

Embedding Model

Document Quality
```

Recommended embedding model:

```text
all-minilm

embeddinggemma
```

---

# Hybrid Retrieval Issues

---

## Problem

Only keyword results appear.

---

## Cause

Vector retrieval unavailable.

---

## Resolution

Verify:

```bash
python scripts/test_semantic_search.py
```

works independently.

---

## Problem

Only semantic results appear.

---

## Cause

Keyword index contains no matching records.

---

## Resolution

Verify catalog metadata.

Review:

```text
Title

Tags

Type

Description
```

---

# Query Interface Issues

---

## Problem

query.py exits immediately.

---

## Cause

Startup exception.

---

## Resolution

Run:

```bash
python scripts/query.py
```

Review stack trace.

Verify:

```text
Catalog

Graph

Vector Store
```

exist.

---

# Ollama Issues

---

## Problem

Connection refused.

Example:

```text
ConnectionError

TimeoutError
```

---

## Resolution

Verify endpoint:

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

## Problem

Embedding model not found.

---

## Resolution

Check:

```bash
curl http://HOST:11434/api/tags
```

Verify model exists.

Example:

```text
all-minilm

embeddinggemma
```

---

## Problem

Embedding generation timeout.

---

## Resolution

Increase timeout.

Verify network connectivity.

Test directly:

```bash
curl http://HOST:11434/api/embed
```

---

# Platform Sync Issues

---

## Problem

platform_sync.py fails.

---

## Resolution

Execute components individually:

```bash
python scripts/knowledge_report.py

python scripts/service_overview.py

python scripts/build_graph.py
```

Identify failing module.

---

# Recovery Procedure

When the platform is in an unknown state:

## Step 1

Rebuild catalog.

```bash
python scripts/platform_sync.py
```

---

## Step 2

Rebuild graph.

```bash
python scripts/build_graph.py
```

---

## Step 3

Rebuild vector index.

```bash
python scripts/build_vector_index.py
```

---

## Step 4

Verify dashboard.

```bash
python scripts/dashboard.py
```

---

## Step 5

Verify search.

```bash
python scripts/query.py
```

---

# Health Verification Checklist

Platform is considered healthy when:

```text
✅ Catalog Exists

✅ Governance Report Generates

✅ Service Catalog Builds

✅ Relationship Graph Builds

✅ Vector Index Builds

✅ Dashboard Generates

✅ Query Interface Responds
```

---

# Log Collection

When raising an issue, capture:

```text
Python Version

requirements.txt

Full Error Message

Stack Trace

Relevant Command Output
```

Example:

```bash
python scripts/query.py \
> logs/query.log 2>&1
```

---

# Quick Command Reference

```bash
python scripts/platform_sync.py

python scripts/build_graph.py

python scripts/build_vector_index.py

python scripts/knowledge_report.py

python scripts/service_overview.py

python scripts/dashboard.py

python scripts/query.py
```

---

# Summary

Most platform issues can be resolved by rebuilding the three core artifacts:

```text
Catalog
      ↓
Relationship Graph
      ↓
Vector Index
```

Recovery workflow:

```bash
python scripts/platform_sync.py

python scripts/build_graph.py

python scripts/build_vector_index.py

python scripts/dashboard.py

python scripts/query.py
```

If all five commands complete successfully, the platform should be operational.