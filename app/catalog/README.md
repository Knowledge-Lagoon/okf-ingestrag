# Catalog Module

## Purpose

The Catalog Module is responsible for building and maintaining the central knowledge inventory of OKF-IngestRAG.

The catalog serves as the platform's source of truth for all validated knowledge assets.

Generated artifact:

```text
catalog/index.json
```

---

## Responsibilities

- Discover OKF documents
- Parse metadata
- Validate content
- Build searchable catalog entries
- Store structured document metadata

---

## Data Flow

```text
OKF Documents
      ↓
Catalog Generator
      ↓
catalog/index.json
```

---

## Catalog Entry Structure

```json
{
  "title": "Kong Restart",
  "type": "runbook",
  "owner": "devops",
  "source": "manual",
  "tags": ["kong", "kubernetes"]
}
```

---

## Consumers

- Search Engine
- Governance
- Service Catalog
- Relationship Graph
- Recommendations
- Context Builder

---

## Summary

The catalog is the central inventory of knowledge assets and the foundation of all discovery and intelligence features.