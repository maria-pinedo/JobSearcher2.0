import unittest
from app.services.matching_engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MatchingEngine()

    def test_keyword_match_scoring(self):
        # 1. Mock Candidate Profile (Output from Phase 1)
        mock_candidate = {
            "skills": ["Python", "SQL", "Power BI", "Forecasting"]
        }

        # 2. Mock Job Posting (Output from Phase 3)
        mock_job = {
            "job_id": "999888777",
            "title": "Data Analyst",
            "company": "Tech Corp",
            "description": "Looking for a Data Analyst with strong Python and SQL experience. Knowledge of Power BI is a plus."
        }

        # 3. Run the evaluation pipeline
        result = self.engine.evaluate_match(mock_candidate, mock_job)

        # 4. Verify the math (Python, SQL, Power BI are present; Forecasting is missing. 3/4 = 75.0)
        self.assertEqual(result["match_score"], 75.0)
        self.assertEqual(result["scoring_method"], "keyword_baseline")
        self.assertEqual(result["company"], "Tech Corp")


if __name__ == "__main__":
    unittest.main()