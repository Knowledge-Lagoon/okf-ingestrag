class PromptBuilder:

    @staticmethod
    def build(
        question: str,
        document_content: str
    ):

        return f"""
You are a DevOps Knowledge Assistant.

Answer ONLY using the supplied knowledge.

Question:
{question}

Knowledge:
{document_content}

Provide a concise answer.
"""