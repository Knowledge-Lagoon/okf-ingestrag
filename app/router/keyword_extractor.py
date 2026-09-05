class KeywordExtractor:

    STOP_WORDS = {
        "how",
        "do",
        "i",
        "what",
        "is",
        "the",
        "a",
        "an",
        "and",
        "to",
        "of",
        "for",
        "in",
        "on",
        "with",
        "tell",
        "me",
        "about",
        "show",
        "explain",
        "can",
        "you",
        "please"
    }

    @staticmethod
    def extract(question: str):

        words = question.lower().split()

        keywords = []

        for word in words:

            cleaned_word = word.strip(".,?!")

            if cleaned_word not in KeywordExtractor.STOP_WORDS:
                keywords.append(cleaned_word)

        return keywords

    @staticmethod
    def primary_keyword(question: str):

        keywords = KeywordExtractor.extract(question)

        if not keywords:
            return ""

        return keywords