import requests
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeetCodeScraper:
    BASE_URL = "https://leetcode.com/api"

    def __init__(self):
        self.session = requests.Session()

    def get_contest_submissions(self, contest_id: str) -> List[Dict]:
        """
        Fetch submissions for a given contest.
        This is a placeholder implementation and needs to be updated with actual LeetCode API endpoints.
        """
        url = f"{self.BASE_URL}/contests/{contest_id}/submissions"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching contest submissions: {e}")
            return []

    def get_submission_details(self, submission_id: str) -> Dict:
        """
        Fetch details for a specific submission.
        This is a placeholder implementation and needs to be updated with actual LeetCode API endpoints.
        """
        url = f"{self.BASE_URL}/submissions/{submission_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching submission details: {e}")
            return {}
        
    def store_submissions(self, submissions: List[Dict]):
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        for submission in submissions:
            db_manager.insert_submission(submission)
        db_manager.close()

if __name__ == "__main__":
    scraper = LeetCodeScraper()
    contest_id = "weekly-contest-123"  # Replace with an actual contest ID
    submissions = scraper.get_contest_submissions(contest_id)
    logger.info(f"Fetched {len(submissions)} submissions for contest {contest_id}")

    scraper.store_submissions(submissions)
    logger.info(f"Stored {len(submissions)} submissions in the database")

    # Fetch and print a sample submission detail
    if submissions:
        sample_submission = submissions[0]
        details = scraper.get_submission_details(sample_submission['id'])
        logger.info(f"Details for submission {sample_submission['id']}: {details}")