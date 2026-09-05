class SearchRanker:

    @staticmethod
    def score(doc, query):

        query = query.lower()

        score = 0

        # Highest weight: title match
        if query in doc.get("title", "").lower():
            score += 10

        # Description match
        if query in doc.get("description", "").lower():
            score += 5

        # Tag matches
        for tag in doc.get("tags", []):

            if query in tag.lower():
                score += 3

        # Content match
        if query in doc.get("content", "").lower():
            score += 1

        return score

    @staticmethod
    def rank(results, query):

        ranked_results = []

        for doc in results:

            doc_score = SearchRanker.score(doc, query)

            doc_copy = doc.copy()
            doc_copy["score"] = doc_score

            ranked_results.append(doc_copy)

        ranked_results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_results