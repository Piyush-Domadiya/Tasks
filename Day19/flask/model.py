from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_score(resume, job):

    text = [resume, job]

    cv = CountVectorizer()

    matrix = cv.fit_transform(text)

    score = cosine_similarity(matrix)[0][1]

    return round(score * 100, 2)