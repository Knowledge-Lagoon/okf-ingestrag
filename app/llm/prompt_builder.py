class PromptBuilder:

    @staticmethod
    def build(question, knowledge):

        return f"""
You are a Senior DevOps Engineer.

Answer ONLY using the supplied knowledge.

Provide:

1. Summary
2. Recommended Action
3. Commands
4. Verification Steps

Question:
{question}

Knowledge:
{knowledge}
"""