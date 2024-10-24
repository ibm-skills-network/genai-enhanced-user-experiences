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
        search_embedding = get_embeddings(query_string)

        # sort issues by their embedding similarity to the query embedding
        sorted_issues = sorted(
            issues, 
            key=lambda issue: cosine_similarity(search_embedding, issue.embedding),
            reverse=False  # lower cosine distance is more similar
        )

        return sorted_issues
