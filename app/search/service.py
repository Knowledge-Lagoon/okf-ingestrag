from app.search.engine import SearchEngine

def search(query, doc_type=None):

    engine = SearchEngine()

    return engine.search(query, doc_type)