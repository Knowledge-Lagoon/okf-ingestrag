# Router Module

## Purpose

The Router determines how user questions should be processed.

---

## Responsibilities

Route queries to appropriate knowledge domains.

Examples:

### Runbook Query

```text
Restart Kong
```

### Service Query

```text
Tell me about Kong
```

### General Knowledge Query

```text
What is CrashLoopBackOff?
```

---

## Data Flow

```text
Question
    ↓
Router
    ↓
Search Strategy
```

---

## Future Evolution

The Router will become the decision layer for:

```text
Keyword Search
Vector Search
Hybrid Retrieval
RAG
```

---

## Summary

The Router selects the most appropriate retrieval strategy for a given question.