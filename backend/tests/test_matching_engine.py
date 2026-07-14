import unittest
from app.services.matching_engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We use setUpClass so the AI model only loads into memory once for all tests
        cls.engine = MatchingEngine()

    def test_blended_match_scoring(self):
        # 1. Mock Candidate Profile
        mock_candidate = {
            "skills": ["Data Visualization", "Statistical Analysis", "Predictive Modeling"]
        }

        # 2. Mock Job Posting (Notice the words are entirely different from the skills!)
        mock_job = {
            "job_id": "111222333",
            "title": "Data Scientist",
            "company": "AI Innovations",
            "description": "Looking for someone to build machine learning models, forecast trends, and create Tableau dashboards."
        }

        # 3. Run the evaluation
        result = self.engine.evaluate_match(mock_candidate, mock_job)

        # 4. Verify outputs
        self.assertEqual(result["keyword_score"], 0.0)  # Proving exact words failed
        self.assertTrue(result["semantic_score"] > 30.0)  # Proving AI understood the context
        self.assertEqual(result["scoring_method"], "blended_nlp")

        print(f"\n--- AI MATCH RESULTS ---")
        print(f"Keyword Score: {result['keyword_score']}%")
        print(f"Semantic Score: {result['semantic_score']}%")
        print(f"Final Blended Score: {result['match_score']}%\n")


if __name__ == "__main__":
    unittest.main()