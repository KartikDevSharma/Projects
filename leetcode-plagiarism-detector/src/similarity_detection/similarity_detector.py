import re
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityDetector:
    def __init__(self):
        self.token_pattern = re.compile(r'\b\w+\b')

    def tokenize(self, code: str) -> List[str]:
        """Convert code string into a list of tokens."""
        return self.token_pattern.findall(code.lower())

    def jaccard_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """Calculate Jaccard similarity between two lists of tokens."""
        set1 = set(tokens1)
        set2 = set(tokens2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def detect_similarities(self, submissions: List[Dict], threshold: float = 0.8) -> List[Tuple[Dict, Dict, float]]:
        """
        Detect similar submissions based on Jaccard similarity.
        Returns a list of tuples (submission1, submission2, similarity_score).
        """
        similar_pairs = []
        n = len(submissions)

        for i in range(n):
            tokens1 = self.tokenize(submissions[i]['preprocessed_code'])
            for j in range(i+1, n):
                tokens2 = self.tokenize(submissions[j]['preprocessed_code'])
                similarity = self.jaccard_similarity(tokens1, tokens2)
                if similarity >= threshold:
                    similar_pairs.append((submissions[i], submissions[j], similarity))

        return similar_pairs

if __name__ == "__main__":
    detector = SimilarityDetector()

    # Test similarity detection
    submissions = [
        {'id': 1, 'preprocessed_code': 'def solution(nums): return sum(nums)'},
        {'id': 2, 'preprocessed_code': 'def answer(numbers): return sum(numbers)'},
        {'id': 3, 'preprocessed_code': 'def solve(arr): total = 0\nfor num in arr:\n    total += num\nreturn total'},
    ]

    similar_pairs = detector.detect_similarities(submissions, threshold=0.5)
    
    for pair in similar_pairs:
        logger.info(f"Similarity detected:")
        logger.info(f"Submission {pair[0]['id']} and Submission {pair[1]['id']}")
        logger.info(f"Similarity score: {pair[2]:.2f}")
        logger.info(f"Code 1: {pair[0]['preprocessed_code']}")
        logger.info(f"Code 2: {pair[1]['preprocessed_code']}")
        logger.info("---")