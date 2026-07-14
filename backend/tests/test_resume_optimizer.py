import unittest
from unittest.mock import patch, MagicMock
import os
from app.services.resume_optimizer import ResumeOptimizer


class TestResumeOptimizer(unittest.TestCase):
    def setUp(self):
        # Inject a dummy key so the test doesn't fail on initialization
        os.environ["GEMINI_API_KEY"] = "dummy_gemini_key"
        self.optimizer = ResumeOptimizer()

    @patch('app.services.resume_optimizer.genai.GenerativeModel.generate_content')
    def test_optimize_resume(self, mock_generate):
        # 1. Define the fake JSON response from Gemini
        mock_response = MagicMock()
        mock_response.text = '''
        {
            "missing_keywords": ["Python", "SQL", "Tableau"],
            "bullet_improvements": [
                {
                    "original": "Created dashboards.",
                    "improved": "Developed interactive Tableau dashboards using SQL data pipelines to track KPIs."
                }
            ],
            "ats_score": 75,
            "skill_gaps": ["Requires more advanced SQL profiling experience."]
        }
        '''
        mock_generate.return_value = mock_response

        # 2. Setup mock inputs
        mock_candidate = {"skills": ["Excel", "Data Entry"]}
        mock_job = "Looking for a Data Analyst with Python, SQL, and Tableau experience."

        # 3. Execute the service method
        result = self.optimizer.optimize(mock_candidate, mock_job)

        # 4. Validate the structured output
        self.assertIsNotNone(result)
        self.assertEqual(result["ats_score"], 75)
        self.assertIn("Python", result["missing_keywords"])
        self.assertEqual(len(result["bullet_improvements"]), 1)
        self.assertIn("Tableau", result["bullet_improvements"][0]["improved"])


if __name__ == "__main__":
    unittest.main()