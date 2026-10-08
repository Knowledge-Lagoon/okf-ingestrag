from pathlib import Path


class GitOKFConverter:

    @staticmethod
    def convert(input_file):

        input_path = Path(input_file)

        title = (
            input_path.stem
            .replace("-", " ")
            .title()
        )

        content = (
            input_path.read_text(
                encoding="utf-8"
            )
        )

        okf_content = f"""---
type: reference
title: {title}
description: Imported from Git
tags:
  - git
  - imported
owner: git-import
source: git
version: 1.0
---

{content}
"""

        output_dir = (
            Path(
                "knowledge/imported"
            )
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_dir
            / input_path.name
        )

        output_file.write_text(
            okf_content,
            encoding="utf-8"
        )

        return str(output_file)