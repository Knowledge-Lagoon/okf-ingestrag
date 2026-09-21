# Assistant Module

The `assistant` module converts retrieved OKF knowledge into a user-facing response.

It provides the presentation layer between the retrieval pipeline and the final user experience. It can return a deterministic response directly from document metadata or later delegate answer generation to the LLM layer.

## Overview

OKF-IngestRAG retrieves knowledge through the following pipeline:

```text
User Question
      |
      v
Keyword Extraction
      |
      v
Query Router
      |
      v
Catalog Search
      |
      v
Search Ranking
      |
      v
Document Retrieval
      |
      v
Assistant
      |
      v
User Response
```

The Assistant module is responsible for converting the selected knowledge document into a clear response.

It does not perform:

- Document ingestion
- OKF validation
- Catalog generation
- Search
- Ranking
- Query routing
- LLM inference

Those responsibilities belong to other modules.

## Directory Structure

```text
app/assistant/
├── __init__.py
├── knowledge_assistant.py
└── README.md
```

Related modules include:

```text
app/router/
app/search/
app/retrieval/
app/llm/
```

## Main Component

### `knowledge_assistant.py`

The `KnowledgeAssistant` class builds a deterministic response from:

- The user's question
- The selected catalog document
- Document metadata
- The source path

Example implementation:

```python
class KnowledgeAssistant:

    @staticmethod
    def build_response(
        question,
        document
    ):

        response = []

        response.append(
            f"Question: {question}"
        )

        response.append("")

        response.append(
            f"Knowledge Match: "
            f"{document['title']}"
        )

        response.append(
            f"Document Type: "
            f"{document['type']}"
        )

        response.append("")

        response.append(
            f"Description: "
            f"{document.get('description', 'N/A')}"
        )

        response.append("")

        response.append(
            f"Source: "
            f"{document['path']}"
        )

        return "\n".join(response)
```

## Example Input

Question:

```text
How do I restart Kong?
```

Selected catalog document:

```python
{
    "title": "Kong Restart",
    "type": "runbook",
    "description": (
        "Procedure to restart Kong deployment "
        "in Kubernetes"
    ),
    "owner": "devops",
    "source": "manual",
    "path": (
        "knowledge/runbooks/"
        "kong-restart.md"
    )
}
```

## Example Output

```text
Question: How do I restart Kong?

Knowledge Match: Kong Restart
Document Type: runbook

Description: Procedure to restart Kong deployment in Kubernetes

Source: knowledge/runbooks/kong-restart.md
```

## Assistant Responsibilities

The Assistant module should:

1. Accept the original user question
2. Accept the selected knowledge document
3. Build a readable response
4. Include the source document
5. Avoid inventing information
6. Keep responses grounded in retrieved knowledge

## Assistant Boundaries

The Assistant module should not:

- Search the catalog directly
- Select the best document
- Read Confluence or Git directly
- Validate OKF frontmatter
- Generate the catalog
- Call connectors
- Modify source documents
- Infer operational steps that do not exist in the retrieved knowledge

Keeping these responsibilities separate makes the platform easier to test and maintain.

## Current Assistant Modes

### Deterministic Mode

The `KnowledgeAssistant` creates a response using catalog metadata.

```text
Question
    |
    v
Selected Document
    |
    v
Formatted Response
```

Advantages:

- No LLM dependency
- Fast response
- Predictable output
- Easy to test
- No hallucination risk from generated text
- Works when Ollama is unavailable

### LLM-Assisted Mode

The LLM path uses:

```text
app/llm/prompt_builder.py
app/llm/ollama_service.py
```

The flow becomes:

```text
Question
    |
    v
Retrieved Documents
    |
    v
Prompt Builder
    |
    v
Remote Ollama
    |
    v
Generated Answer
```

The deterministic Assistant can remain available as a fallback when the remote model is unavailable or times out.

## Relationship With the Search Layer

The Assistant receives results produced by the search pipeline.

```text
app/search/engine.py
        |
        v
app/search/ranker.py
        |
        v
Top Search Result
        |
        v
app/assistant/knowledge_assistant.py
```

The Assistant should not decide which document is most relevant. Search and ranking already make that decision.

## Relationship With the Retrieval Layer

The retrieval layer reads the complete source document.

```text
app/retrieval/retriever.py
```

Example:

```python
content = DocumentRetriever.get_content(
    document["path"]
)
```

The Assistant may use:

- Catalog metadata
- Full document content
- Source path
- Search score
- Related document information

## Relationship With the LLM Layer

The Assistant and LLM modules have different responsibilities.

```text
Assistant
    = response orchestration and formatting

LLM
    = natural-language generation
```

The Assistant may decide whether to:

1. Return a deterministic response
2. Build an LLM prompt
3. Use an LLM-generated response
4. Fall back to deterministic output

Suggested future flow:

```text
Retrieved Knowledge
        |
        v
Assistant
        |
        +---- LLM enabled and available
        |              |
        |              v
        |       Generated Answer
        |
        +---- LLM unavailable
                       |
                       v
              Deterministic Answer
```

## Recommended Source Attribution

Every response should include source information.

Example:

```text
Answer:
Restart the Kong deployment using kubectl.

Source:
knowledge/runbooks/kong-restart.md
```

For multiple documents:

```text
Sources:
- knowledge/runbooks/kong-restart.md
- knowledge/services/kong-service.md
```

Source attribution improves:

- Traceability
- User trust
- Troubleshooting
- Knowledge ownership
- Auditability

## Recommended Response Structure

A future response format can include:

```text
Summary
Recommended Action
Commands
Verification Steps
Sources
```

Example:

```text
Summary

The Kong deployment can be restarted using a Kubernetes rolling restart.

Recommended Action

Restart the Kong deployment in the kong namespace.

Commands

kubectl rollout restart deployment kong -n kong

Verification Steps

kubectl get pods -n kong

Sources

knowledge/runbooks/kong-restart.md
```

The Assistant should only include sections supported by retrieved knowledge.

## Fallback Strategy

The Assistant should handle LLM failures without terminating the application.

Suggested fallback flow:

```text
Call Remote Ollama
        |
        +---- Success
        |       |
        |       v
        |   AI Response
        |
        +---- Timeout or Error
                |
                v
        Deterministic Response
```

Example:

```python
try:

    answer = ollama_service.ask(
        prompt
    )

except Exception:

    answer = (
        KnowledgeAssistant
        .build_response(
            question,
            document
        )
    )
```

A production implementation should catch specific exceptions and log the underlying error.

## Multi-Document Responses

The current retrieval flow can use the highest-ranked result.

```python
document = results[0]
```

A later version can use multiple documents:

```python
top_documents = results[:3]
```

Example:

```text
Question:
Tell me about Kong

Documents:
- Kong API Gateway
- Kong Restart
- Kubernetes Pod Troubleshooting
```

The Assistant can combine those sources into a structured service response.

Care should be taken to avoid sending unrelated or excessive content to the LLM.

## Service-Aware Responses

The Assistant can later integrate with:

```text
app/catalog/service_catalog.py
```

Example:

```text
Service: Kong

Runbooks:
- Kong Restart

Documentation:
- Kong API Gateway

Owners:
- devops
- platform-team

Sources:
- manual
- confluence
- git
```

This provides a more useful answer than presenting unrelated search results.

## Graph-Aware Responses

The Assistant can later integrate with:

```text
app/graph/relationship_graph.py
```

Example:

```text
Selected Document:
Kong Restart

Related Knowledge:
- Kong API Gateway
- Kubernetes Pod Troubleshooting
```

The relationship graph can expand the context while the Assistant controls what appears in the final response.

## Suggested Assistant Interface

A future service interface could be:

```python
class KnowledgeAssistant:

    def answer(
        self,
        question,
        documents,
        use_llm=True
    ):

        pass
```

Inputs:

```text
question
documents
use_llm
```

Output:

```python
{
    "answer": "...",
    "sources": [
        {
            "title": "Kong Restart",
            "path": (
                "knowledge/runbooks/"
                "kong-restart.md"
            )
        }
    ],
    "route": "runbook",
    "llm_used": True
}
```

## Recommended Response Model

A structured response model could contain:

```python
{
    "question": (
        "How do I restart Kong?"
    ),
    "answer": (
        "Restart the Kong deployment "
        "using kubectl."
    ),
    "route": "runbook",
    "sources": [
        {
            "title": "Kong Restart",
            "path": (
                "knowledge/runbooks/"
                "kong-restart.md"
            ),
            "source": "manual",
            "score": 19
        }
    ],
    "related_documents": [],
    "llm_used": False
}
```

Structured output will make it easier to expose the Assistant through:

- FastAPI
- Command-line interfaces
- Web applications
- Chat interfaces
- Other AI agents

## Error Handling

The Assistant should handle:

- Empty questions
- No matching documents
- Missing document metadata
- Missing source files
- Empty document content
- Remote LLM timeout
- Remote LLM connection failure
- Invalid LLM response
- Multiple documents with the same title

Example no-result response:

```text
No matching knowledge was found.

Try using a service name, runbook topic, or technology keyword.
```

Example LLM fallback response:

```text
The AI service is unavailable.

The following knowledge document was found:

Kong Restart
knowledge/runbooks/kong-restart.md
```

## Logging Recommendations

Future Assistant logging should include:

```text
Question received
Router decision
Extracted keywords
Search result count
Selected documents
Prompt size
LLM endpoint used
LLM response status
Fallback activation
Response sources
```

Secrets, tokens, and sensitive document content should not be written to logs.

## Security Considerations

The Assistant may access operational knowledge that includes:

- Internal infrastructure details
- Commands
- Architecture information
- Service dependencies
- Incident procedures
- Internal URLs

Future versions should enforce:

- Source permissions
- Document-level access control
- Sensitive-content filtering
- Secret detection
- Audit logging
- Source attribution

The Assistant should never present knowledge that the requesting user is not authorized to access.

## Testing

Recommended test structure:

```text
tests/
└── assistant/
    ├── test_knowledge_assistant.py
    ├── test_assistant_fallback.py
    └── test_assistant_sources.py
```

Tests should cover:

- Valid document response
- Missing description
- Missing source path
- Empty question
- No search results
- One retrieved document
- Multiple retrieved documents
- LLM success
- LLM timeout
- LLM connectivity failure
- Deterministic fallback
- Source attribution

Example test:

```python
from app.assistant.knowledge_assistant import (
    KnowledgeAssistant
)


def test_build_response():

    document = {
        "title": "Kong Restart",
        "type": "runbook",
        "description": (
            "Restart Kong deployment"
        ),
        "path": (
            "knowledge/runbooks/"
            "kong-restart.md"
        )
    }

    response = (
        KnowledgeAssistant
        .build_response(
            "How do I restart Kong?",
            document
        )
    )

    assert (
        "Kong Restart"
        in response
    )

    assert (
        "knowledge/runbooks/"
        "kong-restart.md"
        in response
    )
```

## Limitations of the Current Version

The current Assistant implementation:

- Uses a simple formatted response
- Expects one selected document
- Does not maintain conversation history
- Does not validate user authorization
- Does not calculate confidence
- Does not automatically use graph relationships
- Does not automatically use the Service Catalog
- Does not provide structured JSON output
- Depends on other modules for retrieval and ranking

These limitations are acceptable for the current MVP.

## Roadmap

### Assistant V1

```text
Deterministic metadata response
Source attribution
Single-document support
```

### Assistant V2

```text
Multiple document support
Structured response model
LLM fallback handling
Improved error messages
```

### Assistant V3

```text
Service Catalog integration
Relationship Graph integration
Confidence indicators
Document-level authorization
```

### Assistant V4

```text
Conversation context
Graph-assisted retrieval
Hybrid RAG
Agentic knowledge exploration
Operational action integration
```

## Usage Example

```python
from app.assistant.knowledge_assistant import (
    KnowledgeAssistant
)


question = "How do I restart Kong?"

document = {
    "title": "Kong Restart",
    "type": "runbook",
    "description": (
        "Procedure to restart Kong "
        "deployment in Kubernetes"
    ),
    "path": (
        "knowledge/runbooks/"
        "kong-restart.md"
    )
}

answer = (
    KnowledgeAssistant
    .build_response(
        question,
        document
    )
)

print(answer)
```

## Summary

The `assistant` module is the user-facing response layer of OKF-IngestRAG.

It transforms:

```text
Question
    +
Retrieved Knowledge
    |
    v
Grounded Response
    +
Source Attribution
```

It provides a stable boundary between the retrieval system and optional LLM-based answer generation.