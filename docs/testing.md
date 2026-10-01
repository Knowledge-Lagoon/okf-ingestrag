# OKF-IngestRAG Testing Guide

## Overview

This document defines the release validation and regression testing process for OKF-IngestRAG version `1.1.0`.

The testing strategy validates:

- OKF document quality
- Catalog generation
- Governance
- Service grouping
- Relationship discovery
- Recommendations
- Context assembly
- Dashboard integration
- Traceable query output
- Connector behavior
- Generated artifact recovery

Vector semantic retrieval is not enabled in version `1.1.0` and is documented separately as future work.

---

## Test Principles

1. Test each module independently before testing integrated flows.
2. Treat Markdown knowledge files as the source of truth.
3. Rebuild generated artifacts rather than editing them manually.
4. Confirm every query response includes sources and paths.
5. Do not block version `1.1.0` on vector or LLM features that are not enabled.
6. Record full stack traces for any unexpected failure.

---

## Test Environment

Verify Python:

```bash
python --version
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run all commands from the repository root.

Verify the release version:

```bash
cat VERSION
```

Expected:

```text
1.1.0
```

---

## Test Data

The release test set should include multiple knowledge types and sources.

Example document types:

- `runbook`
- `service`
- `reference`

Example sources:

- `manual`
- `confluence`
- `git`

Example knowledge areas:

- Kong
- Kubernetes
- EKS
- CrashLoopBackOff
- ImagePullBackOff

Every valid test document should contain:

- `type`
- `title`
- `description`
- `tags`
- `owner`

---

## Test 1: Repository Documentation

Verify root documentation:

```bash
ls README.md CHANGELOG.md VERSION
```

Verify architecture and operational documentation:

```bash
find docs -maxdepth 1 -type f | sort
```

Expected documentation:

```text
docs/architecture.md
docs/data-flow.md
docs/deployment.md
docs/roadmap.md
docs/testing.md
docs/troubleshooting.md
docs/user-guide.md
```

Verify module documentation:

```bash
find app -maxdepth 2 -name README.md | sort
```

Expected module coverage includes:

```text
app/README.md
app/assistant/README.md
app/catalog/README.md
app/connectors/README.md
app/context/README.md
app/dashboard/README.md
app/governance/README.md
app/graph/README.md
app/platform/README.md
app/rag/README.md
app/recommendations/README.md
app/retrieval/README.md
app/router/README.md
app/search/README.md
```

Pass criteria:

- All required documents exist
- No required documentation file is empty

---

## Test 2: Python Import Validation

Compile the application and scripts:

```bash
python -m compileall app scripts
```

Pass criteria:

- No syntax errors
- No missing imports on compiled modules

Optional direct import checks:

```bash
python -c "from app.catalog.generator import CatalogGenerator; print('catalog import ok')"
python -c "from app.governance.report import KnowledgeReport; print('governance import ok')"
python -c "from app.graph.relationship_graph import RelationshipGraph; print('graph import ok')"
python -c "from app.dashboard.dashboard_service import DashboardService; print('dashboard import ok')"
python -c "from app.rag.hybrid_retriever import HybridRetriever; print('retriever import ok')"
```

---

## Test 3: OKF Validation and Catalog Generation

Run:

```bash
python main.py
```

or:

```bash
python scripts/platform_sync.py
```

Verify the catalog exists:

```bash
test -f catalog/index.json && echo "catalog exists"
```

Verify the catalog contains entries:

```bash
python - <<'PY'
import json
from pathlib import Path

path = Path("catalog/index.json")
data = json.loads(path.read_text(encoding="utf-8"))
print(f"catalog entries: {len(data)}")
assert len(data) > 0
PY
```

Pass criteria:

- Catalog generation completes without exceptions
- `catalog/index.json` exists
- Catalog entry count is greater than zero
- Raw staging files are not included
- Invalid OKF documents are excluded

---

## Test 4: Catalog Schema Validation

Run:

```bash
python - <<'PY'
import json
from pathlib import Path

required = {
    "title",
    "type",
    "description",
    "tags",
    "owner",
    "source",
    "path",
    "content",
}

catalog = json.loads(
    Path("catalog/index.json").read_text(encoding="utf-8")
)

for entry in catalog:
    missing = required - entry.keys()
    assert not missing, f"{entry.get('title')} missing {missing}"

print(f"validated {len(catalog)} catalog entries")
PY
```

Pass criteria:

- Every catalog entry contains the required indexed fields

---

## Test 5: Governance

Run:

```bash
python scripts/knowledge_report.py
```

Verify output includes:

- Total Documents
- Knowledge Quality Score
- Documents By Type
- Documents By Source
- Potential Duplicates
- Missing Owners
- Missing Tags
- Missing Descriptions

Release target:

```text
Knowledge Quality Score: 100.0%
Potential Duplicates: None
Missing Owners: None
Missing Tags: None
Missing Descriptions: None
```

A lower score is not automatically a software defect, but unexplained gaps must be reviewed before release.

---

## Test 6: Service Catalog

Run:

```bash
python scripts/service_overview.py
```

Verify:

- At least one service is generated
- Each service contains runbooks or documentation
- Owners, sources, and tags are shown
- Kong documents are grouped together when present

Known limitation:

Service names are inferred from the first word of the title. Values such as `Overview`, `Getting`, `Readme`, or inconsistent capitalization are acceptable for the MVP but should be recorded as backlog improvements.

---

## Test 7: Relationship Graph

Build the graph:

```bash
python scripts/build_graph.py
```

Verify the generated artifact:

```bash
test -f catalog/relationship_graph.json && echo "graph exists"
```

Run the graph report:

```bash
python scripts/relationship_graph_report.py
```

Expected meaningful relationships can include:

```text
Kong Restart <-> Kong API Gateway
EKS Node Failure <-> Kubernetes Pod Troubleshooting
ImagePullBackOff Recovery <-> Kubernetes Pod Troubleshooting
```

Pass criteria:

- Graph artifact exists
- Node count is greater than zero
- At least one meaningful relationship exists when test data shares tags
- Generic source tags do not create noisy relationships
- Documents without meaningful relationships are reported safely

---

## Test 8: Recommendation Engine

Run:

```bash
python scripts/recommendation_report.py
```

Pass criteria:

- Script starts and completes without error
- Existing graph relationships produce ranked recommendations
- Missing recommendations return an empty result or explanatory output rather than a crash

---

## Test 9: Context Builder

Run:

```bash
python scripts/context_report.py
```

Verify the context package includes:

- Query
- Primary document
- Document type
- Source
- Related documents
- Service information
- Runbooks or documentation
- Owners
- Tags

Pass criteria:

- Context is assembled from catalog, graph, and service data
- No required lookup crashes

---

## Test 10: Dashboard Integration

Run:

```bash
python scripts/dashboard.py
```

Verify output includes:

- Total Documents
- Sources
- Quality Score
- Missing metadata counts
- Duplicate count
- Total Services
- Graph Nodes
- Relationships
- Recommendation Paths
- Platform Health

Expected release status:

```text
Platform Health
---------------
HEALTHY
```

This is the primary integration test because it consumes catalog, governance, service, graph, and recommendation metrics together.

---

## Test 11: Query Interface

Run:

```bash
python scripts/query.py
```

Test exact query:

```text
kong
```

Expected behavior:

- Kong-related documents are returned
- Every source includes title, source, and path
- Related knowledge is displayed
- Retrieval trace is displayed
- `Vector Matches` is `0` for version `1.1.0`

Example trace:

```text
Keyword Matches: 2
Vector Matches: 0
Graph Matches: 1
Unique Sources: 2
```

Exit using:

```text
exit
```

Pass criteria:

- No import errors
- No runtime exceptions
- Sources are traceable
- Graph expansion works when relationships exist

---

## Test 12: Search Regression

Test queries:

```text
kong
kubernetes
restart
imagepullbackoff
eks
```

Verify:

- Exact title matches are returned
- Tag matches are returned
- Content-only matches are returned
- Optional document-type filters work
- Results contain ranking scores where expected

---

## Test 13: Confluence Connector

Set environment variables without committing secrets:

```bash
export CONFLUENCE_USERNAME="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-token"
export CONFLUENCE_PAGE_ID="your-page-id"
```

Run:

```bash
python scripts/test_confluence.py
```

Pass criteria:

- Authentication succeeds
- Page ID and title are returned
- Content is non-empty

Test import:

```bash
python scripts/import_confluence_page.py
```

Verify:

- Raw file is created in the staging area
- Converted OKF file is created under `knowledge/imported/`
- Converted file passes validation

Bulk-space listing may depend on API permissions and is not required when single-page import is the validated fallback.

---

## Test 14: Git Connector

Run:

```bash
python scripts/import_git_repo.py
```

Pass criteria:

- Supported documentation files are discovered
- Files are imported without exceptions
- OKF output is created
- Imported documents appear in the regenerated catalog

---

## Test 15: Generated Artifact Recovery

Back up generated files before testing recovery:

```bash
cp catalog/index.json /tmp/index.json.backup
cp catalog/relationship_graph.json /tmp/relationship_graph.json.backup
```

Remove and rebuild the graph:

```bash
rm catalog/relationship_graph.json
python scripts/build_graph.py
```

Pass criteria:

- The graph is recreated successfully

To validate full regeneration, remove the catalog only when the knowledge source files are safe:

```bash
rm catalog/index.json
python scripts/platform_sync.py
```

Pass criteria:

- The catalog is recreated successfully
- Knowledge source files remain unchanged

---

## Test 16: Security and Secret Check

Search for accidental secrets:

```bash
grep -RInE "api[_-]?token|password|secret|bearer" . \
  --exclude-dir=.git \
  --exclude="*.md"
```

Review every match.

Verify `.gitignore` excludes generated or sensitive content as appropriate:

```text
.env
__pycache__/
*.pyc
catalog/index.json
data/chroma/
```

Adjust exclusions to match the repository's release policy.

Pass criteria:

- No real credentials are committed
- Tokens are supplied through environment variables

---

## Test 17: Release Metadata

Verify version:

```bash
cat VERSION
```

Expected:

```text
1.1.0
```

Verify changelog contains the release:

```bash
grep -n "1.1.0" CHANGELOG.md
```

Verify Git working state:

```bash
git status
```

---

## Optional Vector Tests for a Future Release

Vector retrieval is not part of the validated `1.1.0` path.

When implemented, validate in this order:

```bash
python scripts/build_vector_index.py
python scripts/test_semantic_search.py
python scripts/query.py
```

Success criteria:

- Chroma persistence directory exists
- Vector count is greater than zero
- A semantic query finds relevant knowledge without exact wording
- Hybrid query trace reports vector matches greater than zero
- Retrieved chunks include source metadata

Do not mark vector retrieval complete until `SemanticRetriever` exists and is wired into `HybridRetriever`.

---

## Automated Test Recommendations

Future automated tests should be stored under:

```text
tests/
├── assistant/
├── catalog/
├── connectors/
├── context/
├── dashboard/
├── governance/
├── graph/
├── rag/
├── recommendations/
├── router/
└── search/
```

Recommended minimum unit tests:

- Valid and invalid frontmatter
- Catalog exclusion rules
- Search matching and type filters
- Ranking behavior
- Duplicate detection
- Quality score calculation
- Service grouping
- Ignored graph tags
- Relationship scoring
- Context assembly
- Citation deduplication
- Empty result handling
- Missing artifact handling

---

## Release Acceptance Criteria

Release `1.1.0` is accepted when:

```text
Catalog generation             PASS
Governance report              PASS
Service catalog                PASS
Relationship graph             PASS
Recommendation engine          PASS
Context builder                PASS
Dashboard                      PASS
Query interface                PASS
Source attribution             PASS
Documentation                  PASS
Version and changelog          PASS
No critical runtime errors     PASS
```

Known non-blocking limitations:

- Vector retrieval disabled
- Service inference based on titles
- No platform API
- No web UI
- No scheduled synchronization
- No production authorization layer

---

## Suggested Test Record

Record each release test using:

```text
Test:
Command:
Expected Result:
Actual Result:
Status: PASS / FAIL
Notes:
```

Example:

```text
Test: Governance
Command: python scripts/knowledge_report.py
Expected Result: No missing metadata; no exceptions
Actual Result: Quality score 100%; zero issues
Status: PASS
Notes: Release gate satisfied
```

---

## Final Release Sequence

Run:

```bash
python -m compileall app scripts
python scripts/platform_sync.py
python scripts/knowledge_report.py
python scripts/service_overview.py
python scripts/build_graph.py
python scripts/relationship_graph_report.py
python scripts/recommendation_report.py
python scripts/context_report.py
python scripts/dashboard.py
python scripts/query.py
```

If all required tests pass:

```bash
git add .
git commit -m "Release OKF-IngestRAG v1.1.0"
git tag -a v1.1.0 -m "OKF-IngestRAG v1.1.0"
```

---

## Summary

Testing for version `1.1.0` validates the complete governed knowledge-platform path:

```text
Knowledge sources
    ↓
OKF validation
    ↓
Catalog
    ↓
Governance
    ↓
Service catalog
    ↓
Relationship graph
    ↓
Context and recommendations
    ↓
Dashboard
    ↓
Traceable query response
```

Vector semantic retrieval remains a separately testable future enhancement.
