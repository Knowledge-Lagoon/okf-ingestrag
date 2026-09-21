import sys
from pathlib import Path

project_root = (
    Path(__file__).resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(project_root)
)

from app.context.context_builder import (
    ContextBuilder
)

from app.assistant.assistant_v2 import (
    AssistantV2
)


def main():

    document = {
        "title": "Kong Restart",
        "type": "runbook",
        "source": "manual"
    }

    context = (
        ContextBuilder()
        .build(
            "Tell me about Kong",
            document
        )
    )

    response = (
        AssistantV2
        .build_response(
            context
        )
    )

    print(response)


if __name__ == "__main__":
    main()