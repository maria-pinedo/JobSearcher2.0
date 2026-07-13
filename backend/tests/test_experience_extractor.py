import unittest
from app.services.extractors.experience_extractor import ExperienceExtractor


class TestExperienceExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ExperienceExtractor()

    def test_successful_extraction(self):
        sample_resume_text = """
        Data Analyst Intern - Microsoft
        May 2025 - August 2025
        • Developed Power BI dashboards using SQL data pipelines.
        • Improved operational reporting efficiency by 15%.

        Software Engineer | Systems Corp
        January 2023 - Present
        - Built robust backend microservices using Python and Flask.
        """

        results = self.extractor.extract(sample_resume_text)

        self.assertTrue(len(results) >= 2)

        # Verify first entry
        self.assertEqual(results[0]["title"], "Data Analyst Intern")
        self.assertEqual(results[0]["company"], "Microsoft")
        self.assertEqual(results[0]["start_date"], "May 2025")
        self.assertEqual(results[0]["end_date"], "August 2025")
        self.assertIn("Developed Power BI dashboards using SQL data pipelines.", results[0]["responsibilities"])

        # Verify second entry
        self.assertEqual(results[1]["title"], "Software Engineer")
        self.assertEqual(results[1]["company"], "Systems Corp")
        self.assertEqual(results[1]["end_date"], "Present")


if __name__ == "__main__":
    unittest.main()