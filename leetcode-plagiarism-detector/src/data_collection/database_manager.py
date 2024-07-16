from src.similarity_detection.similarity_detector import SimilarityDetector
from src.preprocessing.code_preprocessor import CodePreprocessor
from src.flagging.plagiarism_flagger import PlagiarismFlagger
import sqlite3
from typing import List, Dict, Tuple
import logging
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_name: str = 'leetcode_submissions.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY,
                    contest_id TEXT,
                    user_id TEXT,
                    problem_id TEXT,
                    language TEXT,
                    status TEXT,
                    runtime INTEGER,
                    memory INTEGER,
                    code TEXT,
                    submission_time TIMESTAMP
                )
            ''')
            self.conn.commit()
            logger.info("Tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")

    def insert_submission(self, submission: Dict):
        try:
            self.cursor.execute('''
                INSERT INTO submissions (contest_id, user_id, problem_id, language, status, runtime, memory, code, submission_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                submission['contest_id'],
                submission['user_id'],
                submission['problem_id'],
                submission['language'],
                submission['status'],
                submission['runtime'],
                submission['memory'],
                submission['code'],
                submission['submission_time']
            ))
            self.conn.commit()
            logger.info(f"Inserted submission for user {submission['user_id']}")
        except sqlite3.Error as e:
            logger.error(f"Error inserting submission: {e}")

    def get_submissions(self, contest_id: str) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM submissions WHERE contest_id = ?', (contest_id,))
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error fetching submissions: {e}")
            return []
        
    def get_preprocessed_submissions(self, contest_id: str) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM submissions WHERE contest_id = ?', (contest_id,))
            columns = [column[0] for column in self.cursor.description]
            submissions = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            
            preprocessor = CodePreprocessor()
            for submission in submissions:
                submission['preprocessed_code'] = preprocessor.preprocess(submission['code'], submission['language'])
            
            return submissions
        except sqlite3.Error as e:
            logger.error(f"Error fetching preprocessed submissions: {e}")
            return [] 
              
    def detect_similarities(self, contest_id: str, threshold: float = 0.8) -> List[Tuple[Dict, Dict, float]]:
        submissions = self.get_preprocessed_submissions(contest_id)
        detector = SimilarityDetector()
        return detector.detect_similarities(submissions, threshold)
    
    def flag_plagiarism(self, contest_id: str, similarity_threshold: float = 0.8, flag_threshold: int = 2) -> Dict[int, List[Dict]]:
        similar_pairs = self.detect_similarities(contest_id, similarity_threshold)
        flagger = PlagiarismFlagger(similarity_threshold, flag_threshold)
        return flagger.flag_submissions(similar_pairs)

    def generate_plagiarism_report(self, contest_id: str, similarity_threshold: float = 0.8, flag_threshold: int = 2) -> str:
        flagged_submissions = self.flag_plagiarism(contest_id, similarity_threshold, flag_threshold)
        flagger = PlagiarismFlagger(similarity_threshold, flag_threshold)
        return flagger.generate_report(flagged_submissions)
    
    def get_contests(self) -> List[Dict]:
        try:
            self.cursor.execute('SELECT DISTINCT contest_id FROM submissions')
            contests = self.cursor.fetchall()
            return [{'id': contest[0], 'name': f"Contest {contest[0]}"} for contest in contests]
        except sqlite3.Error as e:
            logger.error(f"Error fetching contests: {e}")
            return []  

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_tables()

    preprocessed_submissions = db_manager.get_preprocessed_submissions('weekly-contest-123')
    logger.info(f"Fetched {len(preprocessed_submissions)} preprocessed submissions for contest weekly-contest-123")
    if preprocessed_submissions:
        logger.info(f"Sample preprocessed code:\n{preprocessed_submissions[0]['preprocessed_code']}")
    similar_pairs = db_manager.detect_similarities('weekly-contest-123', threshold=0.7)
    logger.info(f"Detected {len(similar_pairs)} similar pairs of submissions")
    for pair in similar_pairs:
        logger.info(f"Similarity score: {pair[2]:.2f}")
        logger.info(f"Submission 1 ID: {pair[0]['id']}")
        logger.info(f"Submission 2 ID: {pair[1]['id']}")
        logger.info("---")
    #Test plagiarism flagging and reporting
    contest_id = 'weekly-contest-123'
    report = db_manager.generate_plagiarism_report(contest_id, similarity_threshold=0.7, flag_threshold=2)
    logger.info(f"Plagiarism report for contest {contest_id}:\n{report}")

    db_manager.close()