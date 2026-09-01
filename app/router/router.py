class QueryRouter:

    @staticmethod
    def route(query: str):

        query = query.lower()

        runbook_keywords = [
            "restart",
            "fix",
            "recover",
            "troubleshoot",
            "resolve"
        ]

        service_keywords = [
            "what is",
            "service",
            "application",
            "about"
        ]

        for keyword in runbook_keywords:
            if keyword in query:
                return "runbook"

        for keyword in service_keywords:
            if keyword in query:
                return "service"

        return "general"