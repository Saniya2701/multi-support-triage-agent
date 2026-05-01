from sentence_transformers import SentenceTransformer, util
import torch

class Retriever:
    def __init__(self, documents):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.docs = documents
        self.doc_embeddings = self.model.encode(documents, convert_to_tensor=True)

    def search(self, query, top_k=3):
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        scores = util.pytorch_cos_sim(query_embedding, self.doc_embeddings)[0]
        top_results = torch.topk(scores, k=min(top_k, len(self.docs)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            results.append({
                "doc": self.docs[idx],
                "score": float(score)
            })

        return results