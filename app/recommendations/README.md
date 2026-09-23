# Recommendation Engine

The Recommendation Engine is responsible for identifying additional knowledge that may be useful after a primary document has been selected.

It transforms the platform from a search system into a knowledge guidance system.

---

# Purpose

Traditional search answers:

```text
What matches my query?
```

The Recommendation Engine answers:

```text
What should I look at next?
```

Example:

```text
User Query:
How do I restart Kong?
```

Primary Result:

```text
Kong Restart
```

Recommendations:

```text
Kong API Gateway
CrashLoopBackOff
ImagePullBackOff
```

This allows users to discover related operational knowledge without manually searching for every topic.

---

# Module Structure

```text
app/recommendations/
├── __init__.py
├── recommendation_engine.py
└── README.md
```

Associated script:

```text
scripts/
└── recommendation_report.py
```

---

# Platform Integration

The Recommendation Engine is built on top of the Relationship Graph.

```text
Catalog
   ↓
Relationship Graph
   ↓
Recommendation Engine
```

The recommendation engine does not create relationships.

Its responsibility is to consume existing relationships and provide ranked recommendations.

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

Catalog

        ↓

Relationship Graph

        ↓

Recommendation Engine

        ↓

Assistant
```

---

# Current Recommendation Strategy

Version 1 uses:

```text
Relationship Graph Score
```

Relationships with higher scores are considered more relevant.

Example:

```json
{
  "document": "Kong API Gateway",
  "score": 2,
  "common_tags": [
    "kong",
    "kubernetes"
  ]
}
```

A recommendation score is currently equal to:

```text
Number of shared tags
```

---

# Example

## Document

```text
Kong Restart
```

Tags:

```text
kong
kubernetes
restart
```

---

## Related Document

```text
Kong API Gateway
```

Tags:

```text
kong
kubernetes
api-gateway
```

---

## Relationship

Shared Tags:

```text
kong
kubernetes
```

Score:

```text
2
```

---

## Recommendation

```text
Kong API Gateway
```

Because it has the strongest relationship score.

---

# Main Component

## recommendation_engine.py

Purpose:

```text
Document
        ↓
Related Documents
        ↓
Sort By Score
        ↓
Return Top Recommendations
```

Example usage:

```python
engine = RecommendationEngine()

recommendations = engine.recommend(
    "Kong Restart"
)
```

Result:

```python
[
    {
        "document":
            "Kong API Gateway",
        "score":
            2,
        "common_tags":
            [
                "kong",
                "kubernetes"
            ]
    }
]
```

---

# Recommendation Rules

A recommendation is valid when:

```text
Relationship Graph already contains a relationship
```

Example:

```text
Kong Restart
        |
        +-- Kong API Gateway
```

No relationship:

```text
No recommendation
```

---

# Current Recommendation Ranking

Documents are ranked by:

```text
Highest relationship score first
```

Example:

```text
Score 3
Score 2
Score 1
```

Output:

```text
Score 3
Score 2
Score 1
```

---

# Relationship Sources

Recommendations originate from:

```text
Shared Tags
```

Derived from:

```text
Relationship Graph
```

The Recommendation Engine itself does not analyze document content.

---

# Current Architecture

```text
Question
    ↓

Search
    ↓

Primary Document
    ↓

Recommendation Engine
    ↓

Related Knowledge
```

Example:

```text
Question:
Tell me about Kong

Primary:
Kong API Gateway

Recommended:
Kong Restart
CrashLoopBackOff
```

---

# Assistant Integration

Assistant V2 can consume recommendations.

Current flow:

```text
Question
    ↓

Primary Result
```

Future flow:

```text
Question
    ↓

Primary Result
    ↓

Recommended Knowledge
```

Example response:

```text
Primary Knowledge

Kong API Gateway

Recommended Knowledge

- Kong Restart
- CrashLoopBackOff
```

---

# Service Catalog Integration

The Recommendation Engine complements the Service Catalog.

Service Catalog:

```text
Service: Kong

Runbooks:
- Kong Restart

Documentation:
- Kong API Gateway
```

Recommendation Engine:

```text
Primary:
Kong API Gateway

Recommended:
Kong Restart
```

---

# Context Builder Integration

The Context Builder can enrich AI prompts using recommendations.

Instead of:

```text
Question
↓
Single Document
↓
LLM
```

Future workflow:

```text
Question
↓
Document
↓
Recommendations
↓
Expanded Context
↓
LLM
```

---

# Example Context Package

```json
{
  "query":
      "Tell me about Kong",

  "primary_document":
      "Kong API Gateway",

  "recommended_documents":
      [
          "Kong Restart"
      ]
}
```

---

# Future Recommendation Strategies

## V2

Relationship Score Weighting

Example:

```text
Shared Tags
+
Service Match
+
Source Match
```

---

## V3

Service-Based Recommendations

Example:

```text
Service: Kong

Recommended
-----------
Kong Restart
Kong API Gateway
```

---

## V4

Graph Expansion

Current:

```text
Primary Document
↓
Direct Relationships
```

Future:

```text
Primary Document
↓
Direct Relationships
↓
Secondary Relationships
```

---

# Recommendation Quality

Higher scores imply stronger relationships.

Example:

```text
Score 1
========
Weak

Score 2
========
Medium

Score 3+
========
Strong
```

These categories are conceptual and not yet implemented.

---

# Limitations

Current limitations:

```text
Shared-tag relationships only
```

No support yet for:

```text
Service dependencies
Technology dependencies
Owner relationships
Document popularity
Usage statistics
```

---

# Error Handling

When a document has no graph entry:

```python
[]
```

An empty recommendation list is returned.

Example:

```text
No recommendations found.
```

The engine should not fail because recommendations are optional.

---

# Testing

Execute:

```bash
python scripts/recommendation_report.py
```

Expected output:

```text
Recommendations
==================================================

Primary Document:
Kong Restart

Recommended Knowledge
------------------------------

- Kong API Gateway
  Score: 2
  Tags: kong, kubernetes
```

---

# Roadmap

## V1 ✅

```text
Relationship Graph Integration
Score-Based Ranking
Top-N Recommendations
```

## V2

```text
Relationship Weighting
Service Awareness
```

## V3

```text
Context-Aware Recommendations
Assistant Integration
```

## V4

```text
Graph Expansion
Impact Analysis
Knowledge Navigation
```

---

# Summary

The Recommendation Engine provides the transition from:

```text
Search Engine
```

to:

```text
Knowledge Guidance Platform
```

It helps users move beyond a single document and explore the most relevant related knowledge available within the OKF-IngestRAG ecosystem.