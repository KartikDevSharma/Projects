import unittest
from src.data_collection.leetcode_scraper import LeetCodeScraper
from src.data_collection.database_manager import DatabaseManager

class TestDataCollection(unittest.TestCase):
    def setUp(self):
        self.scraper = LeetCodeScraper()
        self.db_manager = DatabaseManager(':memory:')  # Use in-memory database for testing
        self.db_manager.connect()
        self.db_manager.create_tables()

    def tearDown(self):
        self.db_manager.close()

    def test_get_contest_submissions(self):
        contest_id = "weekly-contest-123"
        submissions = self.scraper.get_contest_submissions(contest_id)
        self.assertIsInstance(submissions, list)
        # Add more specific assertions based on the expected structure of submissions

    def test_insert_submission(self):
        sample_submission = {
            'contest_id': 'weekly-contest-123',
            'user_id': 'user123',
            'problem_id': 'problem456',
            'language': 'python3',
            'status': 'Accepted',
            'runtime': 100,
            'memory': 16000,
            'code': 'def solution(nums): return sum(nums)',
            'submission_time': '2023-07-16 10:30:00'
        }
        self.db_manager.insert_submission(sample_submission)
        
        # Verify the submission was inserted
        submissions = self.db_manager.get_submissions('weekly-contest-123')
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0]['user_id'], 'user123')

if __name__ == '__main__':
    unittest.main()