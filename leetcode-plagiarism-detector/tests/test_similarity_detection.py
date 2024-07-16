import unittest
from src.similarity_detection.similarity_detector import SimilarityDetector

class TestSimilarityDetection(unittest.TestCase):
    def setUp(self):
        self.detector = SimilarityDetector()

    def test_tokenize(self):
        code = "def func(a, b): return a + b"
        tokens = self.detector.tokenize(code)
        self.assertEqual(tokens, ['def', 'func', 'a', 'b', 'return', 'a', 'b'])

    def test_jaccard_similarity(self):
        tokens1 = ['a', 'b', 'c', 'd']
        tokens2 = ['a', 'b', 'e', 'f']
        similarity = self.detector.jaccard_similarity(tokens1, tokens2)
        self.assertEqual(similarity, 0.5)

    def test_detect_similarities(self):
        submissions = [
            {'id': 1, 'preprocessed_code': 'def func(a, b): return a + b'},
            {'id': 2, 'preprocessed_code': 'def add(x, y): return x + y'},
            {'id': 3, 'preprocessed_code': 'def subtract(a, b): return a - b'},
        ]
        similar_pairs = self.detector.detect_similarities(submissions, threshold=0.5)
        self.assertEqual(len(similar_pairs), 1)
        self.assertEqual(similar_pairs[0][0]['id'], 1)
        self.assertEqual(similar_pairs[0][1]['id'], 2)

if __name__ == '__main__':
    unittest.main()