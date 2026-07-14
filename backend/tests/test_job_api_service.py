import unittest
from unittest.mock import patch
import os
from app.services.job_api_service import AdzunaClient

class TestJobApiService(unittest.TestCase):
    def setUp(self):
        # We temporarily inject dummy keys into the environment for testing purposes
        # so the test doesn't fail if it's ever run on a CI/CD server without a .env file.
        os.environ["ADZUNA_APP_ID"] = "dummy_id"
        os.environ["ADZUNA_APP_KEY"] = "dummy_key"
        self.client = AdzunaClient()

    # The @patch decorator intercepts the requests.get call before it hits the internet
    @patch('app.services.job_api_service.requests.get')
    def test_search_jobs_normalization(self, mock_get):
        # 1. Define the fake JSON response that mimics Adzuna's actual structure
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 123456789,
                    "title": "Data Analyst Intern",
                    "company": {"display_name": "Microsoft"},
                    "location": {"display_name": "Seattle, WA"},
                    "description": "SQL and Python skills required.",
                    "redirect_url": "https://example.com/job/123",
                    "salary_min": 60000,
                    "salary_max": 80000
                }
            ]
        }

        # 2. Execute the service method
        results = self.client.search_jobs(query="Data Analyst", location="US", limit=1)

        # 3. Validate that our normalization logic successfully transformed the raw payload
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["job_id"], "123456789")
        self.assertEqual(results[0]["title"], "Data Analyst Intern")
        self.assertEqual(results[0]["company"], "Microsoft")
        self.assertEqual(results[0]["location"], "Seattle, WA")
        self.assertEqual(results[0]["salary_min"], 60000)
        self.assertIn("job_id", results[0])
        self.assertIn("url", results[0])

if __name__ == "__main__":
    unittest.main()