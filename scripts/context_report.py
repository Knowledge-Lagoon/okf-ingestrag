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


def main():

    document = {
        "title": "Kong Restart",
        "type": "runbook",
        "source": "manual"
    }

    builder = (
        ContextBuilder()
    )

    context = (
        builder.build(
            "Tell me about Kong",
            document
        )
    )

    print(
        "\nContext Package"
    )

    print(
        "=" * 50
    )

    for (
        key,
        value
    ) in context.items():

        print(
            f"\n{key}"
        )

        print(
            value
        )


if __name__ == "__main__":
    main()