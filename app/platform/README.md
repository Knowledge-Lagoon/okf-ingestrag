# Platform Service

The Platform Service is the orchestration layer of OKF-IngestRAG.

Its purpose is to provide a single entry point that coordinates knowledge ingestion, governance, discovery, relationship generation, and platform health operations.

It transforms the system from a collection of individual modules into a cohesive platform.

---

# Purpose

During development, individual capabilities can be executed independently:

```bash
python scripts/import_confluence_page.py

python scripts/import_git_repo.py

python scripts/build_graph.py

python scripts/knowledge_report.py

python scripts/service_overview.py
```

These scripts are useful for testing individual capabilities.

In a production platform, users should not need to know which internal components exist.

The Platform Service provides a unified orchestration layer.

---

# Platform Responsibilities

The Platform Service coordinates:

```text
Knowledge Sources
        ↓

Catalog Generation

        ↓

Governance

        ↓

Service Catalog

        ↓

Relationship Graph

        ↓

Recommendations

        ↓

Context Generation

        ↓

Assistant
```

The Platform Service does not replace those modules.

It acts as the central coordinator.

---

# Module Structure

```text
app/platform/
├── __init__.py
├── platform_service.py
└── README.md
```

Associated execution script:

```text
scripts/
└── platform_sync.py
```

---

# Why the Platform Service Exists

Without orchestration:

```text
Import
     ↓

Generate Catalog
     ↓

Build Graph
     ↓

Generate Governance Report
     ↓

Build Recommendations
```

are all executed separately.

With the Platform Service:

```text
Platform Sync
      ↓

Everything Refreshes
```

from a single command.

---

# Platform Architecture

```text
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

Governance

        ↓

Service Catalog

        ↓

Relationship Graph

        ↓

Recommendation Engine

        ↓

Context Builder

        ↓

Assistant
```

The Platform Service orchestrates this workflow.

---

# Current Responsibilities

## Catalog Refresh

The platform regenerates:

```text
catalog/index.json
```

The catalog is the searchable inventory of valid OKF knowledge.

---

## Governance

The platform executes:

```text
Knowledge Quality Analysis
```

Including:

- Total Documents
- Documents by Type
- Documents by Source
- Duplicate Detection
- Missing Tags
- Missing Owners
- Missing Descriptions
- Knowledge Quality Score

---

## Service Catalog

The platform builds:

```text
Service Awareness
```

Example:

```text
Kong

├── Runbooks
├── Documentation
├── Sources
├── Owners
└── Tags
```

---

## Relationship Graph

The platform builds relationships between documents.

Example:

```text
Kong Restart
      │
      └── Kong API Gateway
```

Output:

```text
catalog/relationship_graph.json
```

---

## Recommendation Engine

The platform can generate:

```text
Suggested Knowledge
```

based on relationships.

Example:

```text
Primary:
Kong Restart

Recommended:
Kong API Gateway
CrashLoopBackOff
```

---

## Context Builder

The platform assembles:

```text
Context Packages
```

for Assistant and AI use.

Example:

```json
{
    "query":
        "Tell me about Kong",

    "primary_document":
        "Kong API Gateway",

    "related_documents":
        [
            "Kong Restart"
        ]
}
```

---

# Current Implementation

## platform_service.py

The Platform Service currently supports:

```python
PlatformService

├── sync()
```

The sync operation performs:

```text
Catalog Refresh
        ↓

Governance Report
        ↓

Service Catalog
        ↓

Relationship Graph
```

---

# Example Usage

```python
from app.platform.platform_service import (
    PlatformService
)

platform = PlatformService()

platform.sync()
```

---

# Example Sync Execution

```bash
python scripts/platform_sync.py
```

Output:

```text
Platform Sync
==================================================

Catalog Entries: 13

Generating Governance Report...

Knowledge Quality Score: 96%

Services: 4

Graph Nodes: 13

Platform Sync Complete
```

---

# Data Flow

```text
Knowledge Sources

Filesystem
Confluence
Git

        ↓

OKF Documents

        ↓

Validation

        ↓

Catalog

        ↓

Platform Service

        ↓

Governance
Service Catalog
Relationship Graph
Recommendations

        ↓

Assistant
```

---

# Planned Responsibilities

## Ingestion Coordination

Future versions may coordinate:

```text
Confluence Import
Git Import
Filesystem Discovery
```

through a single operation.

Example:

```python
PlatformService.sync()
```

would perform:

```text
Import
 ↓
Convert
 ↓
Validate
 ↓
Catalog
 ↓
Governance
```

---

## Assistant Integration

Future flow:

```text
Question
    ↓

Platform Service

    ↓

Search

    ↓

Context Builder

    ↓

Assistant
```

This simplifies the application's public interface.

---

## Dashboard Integration

The platform service will eventually feed:

```text
Knowledge Dashboard
```

Metrics such as:

```text
Total Documents
Services
Relationships
Recommendations
Quality Score
```

can be generated centrally.

---

# Relationship With Other Modules

## Catalog

Provides:

```text
Knowledge Inventory
```

Consumed by:

```text
Platform Service
```

---

## Governance

Provides:

```text
Knowledge Quality
```

Consumed by:

```text
Platform Service
```

---

## Service Catalog

Provides:

```text
Service Awareness
```

Consumed by:

```text
Platform Service
```

---

## Relationship Graph

Provides:

```text
Knowledge Relationships
```

Consumed by:

```text
Platform Service
```

---

## Recommendation Engine

Provides:

```text
Suggested Knowledge
```

Consumed by:

```text
Platform Service
```

---

## Context Builder

Provides:

```text
AI Context Packages
```

Consumed by:

```text
Platform Service
```

---

## Assistant

Provides:

```text
User Response Generation
```

Consumed by:

```text
Platform Service
```

---

# Design Principles

## Centralized Orchestration

Business workflows should be coordinated through one layer.

```text
Platform Service
```

becomes the platform entry point.

---

## Loose Coupling

Modules remain independent.

Example:

```text
Governance
```

should not directly call:

```text
Assistant
```

The Platform Service coordinates them.

---

## Reusable Components

Every module should still be executable independently.

Example:

```text
Governance
Service Catalog
Relationship Graph
```

can all run without the platform layer.

The Platform Service simply combines them.

---

## AI Independence

The Platform Service works with or without an LLM.

Current:

```text
Knowledge Platform
```

Future:

```text
Knowledge Platform
      +
     AI
```

The platform should remain fully functional even if AI components are unavailable.

---

# Error Handling

Platform execution should continue whenever possible.

Example:

```text
Catalog Success

Graph Failure

Governance Success
```

should not terminate the entire platform sync.

Future versions should isolate failures and provide execution status per component.

Example:

```python
{
    "catalog": "success",
    "graph": "failed",
    "governance": "success"
}
```

---

# Roadmap

## Platform Service V1 ✅

```text
Catalog Refresh
Governance
Service Catalog
Relationship Graph
```

---

## Platform Service V2

```text
Confluence Import
Git Import
Recommendation Refresh
Context Refresh
```

---

## Platform Service V3

```text
Dashboard Integration
Assistant Integration
```

---

## Platform Service V4

```text
LLM Integration
Graph-Assisted Context
AI Workflows
```

---

# Testing

Execute:

```bash
python scripts/platform_sync.py
```

Expected:

```text
Platform Sync
==================================================

Catalog Entries: 13

Knowledge Quality Score: 96%

Services: 4

Graph Nodes: 13

Platform Sync Complete
```

---

# Summary

The Platform Service is the orchestration layer of OKF-IngestRAG.

It transforms a collection of independent modules into a coordinated knowledge platform.

```text
Knowledge Sources
        ↓

Catalog

        ↓

Governance

        ↓

Relationships

        ↓

Recommendations

        ↓

Context

        ↓

Assistant
```

It serves as the foundation for future dashboards, AI integration, and enterprise-scale knowledge operations.