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

from app.platform.platform_service import (
    PlatformService
)


def main():

    service = (
        PlatformService()
    )

    service.sync()


if __name__ == "__main__":
    main()