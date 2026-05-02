import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_all_documents(company):
    """Load documents from company folder"""
    all_docs = []
    base_path = "../data"
    
    if company and company.lower() in ["hackerrank", "claude", "visa"]:
        company_path = os.path.join(base_path, company.lower())
    else:
        company_path = base_path
    
    # Recursively load all files
    if os.path.exists(company_path):
        for root, dirs, files in os.walk(company_path):
            for file in files:
                if file.endswith(('.txt', '.md')):
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().strip()
                            if content and len(content) > 30:  # Only keep non-empty docs
                                all_docs.append(content)
                    except Exception as e:
                        pass  # Skip problematic files
    
    return all_docs

def retrieve_documents(query, company=""):
    """
    Retrieve best matching document using TF-IDF
    
    Args:
        query: User's question/issue
        company: Company name (hackerrank, claude, visa, or empty)
    
    Returns:
        (document_text, similarity_score) or (None, 0.0)
    """
    
    # Load documents
    all_docs = load_all_documents(company)
    
    # If no docs found, return None
    if not all_docs or len(all_docs) < 2:
        return None, 0.0
    
    try:
        # TF-IDF with safe parameters
        vectorizer = TfidfVectorizer(
            max_features=300,           # Reduced to avoid sparse matrix
            stop_words='english',
            min_df=1,
            max_df=0.95,
            ngram_range=(1, 2),
            lowercase=True,
            strip_accents='ascii'
        )
        
        # Fit and transform all documents
        vectors = vectorizer.fit_transform(all_docs)
        
        # Transform the query
        if len(query.strip()) == 0:
            return None, 0.0
        
        query_vec = vectorizer.transform([query])
        
        # Compute similarity scores
        scores = cosine_similarity(query_vec, vectors)[0]
        
        if len(scores) == 0 or np.max(scores) == 0:
            return None, 0.0
        
        # Get best match
        best_idx = np.argmax(scores)
        best_score = float(scores[best_idx])
        best_doc = all_docs[best_idx]
        
        # Return truncated document and score
        return best_doc[:500], best_score
    
    except Exception as e:
        # Fail gracefully
        return None, 0.0