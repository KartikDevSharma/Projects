from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlagiarismFlagger:
    def __init__(self, similarity_threshold: float = 0.8, flag_threshold: int = 2):
        self.similarity_threshold = similarity_threshold
        self.flag_threshold = flag_threshold

    def flag_submissions(self, similar_pairs: List[Tuple[Dict, Dict, float]]) -> Dict[int, List[Dict]]:
        """
        Flag submissions that appear in multiple similar pairs.
        Returns a dictionary with submission IDs as keys and lists of similar submissions as values.
        """
        submission_flags = {}

        for sub1, sub2, similarity in similar_pairs:
            if similarity >= self.similarity_threshold:
                self._add_flag(submission_flags, sub1['id'], sub2)
                self._add_flag(submission_flags, sub2['id'], sub1)

        # Filter out submissions that don't meet the flag threshold
        return {sub_id: flags for sub_id, flags in submission_flags.items() if len(flags) >= self.flag_threshold}

    def _add_flag(self, submission_flags: Dict[int, List[Dict]], sub_id: int, similar_sub: Dict):
        if sub_id not in submission_flags:
            submission_flags[sub_id] = []
        submission_flags[sub_id].append(similar_sub)

    def generate_report(self, flagged_submissions: Dict[int, List[Dict]]) -> str:
        """Generate a report of flagged submissions."""
        report = "Plagiarism Detection Report\n"
        report += "===========================\n\n"

        for sub_id, similar_subs in flagged_submissions.items():
            report += f"Submission ID: {sub_id}\n"
            report += f"Number of similar submissions: {len(similar_subs)}\n"
            report += "Similar submissions:\n"
            for similar_sub in similar_subs:
                report += f"  - Submission ID: {similar_sub['id']}\n"
            report += "\n"

        return report

if __name__ == "__main__":
    flagger = PlagiarismFlagger(similarity_threshold=0.7, flag_threshold=2)

    # Test flagging system
    similar_pairs = [
        ({'id': 1, 'user_id': 'user1'}, {'id': 2, 'user_id': 'user2'}, 0.9),
        ({'id': 1, 'user_id': 'user1'}, {'id': 3, 'user_id': 'user3'}, 0.8),
        ({'id': 2, 'user_id': 'user2'}, {'id': 3, 'user_id': 'user3'}, 0.75),
        ({'id': 4, 'user_id': 'user4'}, {'id': 5, 'user_id': 'user5'}, 0.95),
    ]

    flagged_submissions = flagger.flag_submissions(similar_pairs)
    logger.info(f"Flagged submissions: {flagged_submissions}")

    report = flagger.generate_report(flagged_submissions)
    logger.info(f"Plagiarism report:\n{report}")