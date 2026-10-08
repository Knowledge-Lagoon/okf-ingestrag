class KnowledgeAssistant:

    @staticmethod
    def build_response(question, document):

        response = []

        response.append(f"Question: {question}")
        response.append("")
        response.append(f"Knowledge Match: {document['title']}")
        response.append(f"Document Type: {document['type']}")
        response.append("")
        response.append(f"Description: {document.get('description', 'N/A')}")
        response.append("")
        response.append(f"Source: {document['path']}")

        return "\n".join(response)