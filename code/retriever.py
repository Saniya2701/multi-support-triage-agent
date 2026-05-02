import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 📚 Load documents from folders
def load_documents():
    base_path = "../data"

    docs = {
        "hackerrank": [],
        "claude": [],
        "visa": []
    }

    for company in docs.keys():
        folder = os.path.join(base_path, company)

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):
            try:
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    docs[company].append(f.read())
            except:
                continue

    return docs


# 📦 Initialize (runs once)
documents = load_documents()

all_docs = []
doc_company_map = []

for company, docs_list in documents.items():
    for doc in docs_list:
        all_docs.append(doc)
        doc_company_map.append(company)

# 🧠 TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(all_docs)


# 🔍 Main retrieval function (THIS FIXES YOUR ERROR)
def retrieve_documents(query, company):
    if not query.strip():
        return "", 0.0

    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, doc_vectors).flatten()

    # Filter docs by company
    best_score = 0
    best_doc = ""

    for i, score in enumerate(similarities):
        if doc_company_map[i] == company.lower():
            if score > best_score:
                best_score = score
                best_doc = all_docs[i]

    return best_doc, float(best_score)