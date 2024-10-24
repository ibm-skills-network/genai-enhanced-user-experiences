from models import Issue, Story, Bug, Epic
from embeddings import get_embeddings
from scipy.spatial.distance import cosine

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    if vec1 and vec2:
        return float(cosine(vec1, vec2))  # ensure the result is a plain float
    return 1.0  # return maximum distance if any of the embeddings is missing

def simple_search(query_string: str):
    return Issue.query.filter(Issue.title.ilike(f'%{query_string}%')).all()
    
def semantic_search(query_string: str):
    query = Issue.query

    issues = query.all()

    if query:
        # generate embedding for the search query
        # TODO: your code here

        # sort issues by their embedding similarity to the query embedding
        #TODO: sorted_issues = ...
        # return sorted_issues
        pass # TODO: remove 
