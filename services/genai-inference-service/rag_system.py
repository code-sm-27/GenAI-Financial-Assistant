# services/genai-inference-service/rag_system.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleRAG:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self._load_corpus()

    def _load_corpus(self):
        """Loads documents from the corpus file."""
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split content by a unique separator (e.g., "--- Doc X ---")
                raw_docs = content.split('--- Doc')[1:] # Skip the first empty split
                for i, doc in enumerate(raw_docs):
                    # Remove the doc number line (e.g., " 1 ---") and clean whitespace
                    cleaned_doc = doc.split('---', 1)[1].strip()
                    self.documents.append(cleaned_doc)
            logging.info(f"Loaded {len(self.documents)} documents from corpus.")
            self._build_tfidf_matrix()
        except FileNotFoundError:
            logging.error(f"Corpus file not found: {self.corpus_path}")
            self.documents = []
        except Exception as e:
            logging.error(f"Error loading corpus: {e}")
            self.documents = []

    def _build_tfidf_matrix(self):
        """Builds the TF-IDF matrix from the loaded documents."""
        if self.documents:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
            logging.info("TF-IDF matrix built.")
        else:
            self.tfidf_matrix = None
            logging.warning("No documents to build TF-IDF matrix.")

    def retrieve_context(self, query: str, top_k: int = 2) -> list:
        """
        Retrieves the most relevant documents from the corpus based on the query.
        """
        if not self.documents or self.tfidf_matrix is None:
            logging.warning("RAG system not initialized with a corpus.")
            return []

        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get indices of top_k most similar documents
            top_indices = similarities.argsort()[-top_k:][::-1] # Sort in descending order
            
            context = []
            for i in top_indices:
                if similarities[i] > 0.1: # Threshold to avoid irrelevant docs
                    context.append(self.documents[i])
                    logging.debug(f"Retrieved context (similarity: {similarities[i]:.2f}): {self.documents[i][:100]}...")
            return context
        except Exception as e:
            logging.error(f"Error retrieving context: {e}")
            return []

# Example usage (for testing RAG system directly)
if __name__ == '__main__':
    corpus_file = 'financial_corpus/sample_docs.txt'
    rag = SimpleRAG(corpus_file)

    print("\nQuery 1: What is an SIP?")
    context1 = rag.retrieve_context("What is a SIP investment plan in India?")
    for i, doc in enumerate(context1):
        print(f"Context {i+1}:\n{doc}\n---")

    print("\nQuery 2: How does SEBI regulate financial markets?")
    context2 = rag.retrieve_context("Tell me about the role of SEBI in India.")
    for i, doc in enumerate(context2):
        print(f"Context {i+1}:\n{doc}\n---")

    print("\nQuery 3: Give me some details about equity and debt funds.")
    context3 = rag.retrieve_context("Difference between equity and debt mutual funds.")
    for i, doc in enumerate(context3):
        print(f"Context {i+1}:\n{doc}\n---")

    print("\nQuery 4: Something irrelevant.")
    context4 = rag.retrieve_context("What is the capital of France?")
    for i, doc in enumerate(context4):
        print(f"Context {i+1}:\n{doc}\n---") # Should return empty or very low relevance