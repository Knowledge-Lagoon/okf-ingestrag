class PromptBuilder:

    @staticmethod
    def build(question, document_content):

        return f"""
You are a DevOps Knowledge Assistant.

Use ONLY the supplied document.

Question:
{question}

Knowledge:
{document_content}

Provide a concise answer.
"""