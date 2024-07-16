import unittest
from src.flagging.plagiarism_flagger import PlagiarismFlagger

class TestFlagging(unittest.TestCase):
    def setUp(self):
        self.flagger = PlagiarismFlagger(similarity_threshold=0.7, flag_threshold=2)

    def test_flag_submissions(self):
        similar_pairs = [
            ({'id': 1, 'user_id': 'user1'}, {'id': 2, 'user_id': 'user2'}, 0.9),
            ({'id': 1, 'user_id': 'user1'}, {'id': 3, 'user_id': 'user3'}, 0.8),
            ({'id': 2, 'user_id': 'user2'}, {'id': 3, 'user_id': 'user3'}, 0.75),
            ({'id': 4, 'user_id': 'user4'}, {'id': 5, 'user_id': 'user5'}, 0.95),
        ]
        flagged = self.flagger.flag_submissions(similar_pairs)
        self.assertEqual(len(flagged), 3)  # submissions 1, 2, and 3 should be flagged
        self.assertIn(1, flagged)
        self.assertIn(2, flagged)
        self.assertIn(3, flagged)

    def test_generate_report(self):
        flagged_submissions = {
            1: [{'id': 2, 'user_id': 'user2'}, {'id': 3, 'user_id': 'user3'}],
            2: [{'id': 1, 'user_id': 'user1'}, {'id': 3, 'user_id': 'user3'}],
        }
        report = self.flagger.generate_report(flagged_submissions)
        self.assertIn("Submission ID: 1", report)
        self.assertIn("Submission ID: 2", report)
        self.assertIn("Number of similar submissions: 2", report)

if __name__ == '__main__':
    unittest.main()