from app.search.engine import SearchEngine


def search(query):

    engine = SearchEngine()

    return engine.search(query)