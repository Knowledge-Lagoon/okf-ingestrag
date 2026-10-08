# Connectors Module

## Purpose

Connectors import knowledge from external sources and convert content into OKF-compliant documents.

---

## Supported Sources

### Filesystem

```text
Markdown
Runbooks
Documentation
```

### Confluence

```text
Pages
Spaces
Exports
```

### Git

```text
README Files
Documentation
Runbooks
```

---

## Data Flow

```text
Source
   ↓
Connector
   ↓
OKF Conversion
   ↓
Knowledge Repository
```

---

## Responsibilities

- Connect to external systems
- Retrieve content
- Convert to markdown
- Generate OKF documents
- Preserve source metadata

---

## Summary

Connectors are responsible for acquiring knowledge and normalizing it into the OKF standard.