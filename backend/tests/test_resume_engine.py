import unittest
from app.services.resume_engine import ResumeEngine


class TestResumeEngineIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = ResumeEngine()

    def test_complete_resume_pipeline(self):
        # A full, multi-section mock resume designed to test all 5 extractors simultaneously
        sample_resume = """
        Maria Jose Pinedo Velarde
        maria@email.com
        (555) 555-1234

        Appalachian State University
        Master of Science in Applied Data Analytics
        Expected Graduation: December 2026

        Python
        SQL
        Power BI
        Forecasting

        Professional Experience:
        Data Analyst Intern - Microsoft
        May 2025 - August 2025
        • Developed Power BI dashboards using SQL data pipelines.
        • Improved operational reporting efficiency by 15%.

        Academic Projects:
        Power BI Sales Dashboard
        Tools: Power BI, SQL, Excel
        • Developed interactive sales dashboards tracking $2M in revenue.
        """

        # Run the full resume pipeline using your engine's method
        profile = self.engine.build_profile(sample_resume)

        # 1. Validate all keys exist in the output candidate profile dictionary
        self.assertIn("contact", profile)
        self.assertIn("skills", profile)
        self.assertIn("education", profile)
        self.assertIn("experience", profile)
        self.assertIn("project", profile)

        # 2. Validate Contact Extractor output
        self.assertEqual(profile["contact"]["email"], "maria@email.com")
        self.assertEqual(profile["contact"]["phone"], "(555) 555-1234")

        # 3. Validate Skill Extractor output
        self.assertIn("Python", profile["skills"])
        self.assertIn("SQL", profile["skills"])
        self.assertIn("Power BI", profile["skills"])

        # 4. Validate Education Extractor output
        self.assertTrue(len(profile["education"]) > 0)
        self.assertEqual(profile["education"][0]["school"], "Appalachian State University")
        self.assertEqual(profile["education"][0]["degree"], "Master of Science")

        # 5. Validate Experience Extractor output
        self.assertTrue(len(profile["experience"]) > 0)
        self.assertEqual(profile["experience"][0]["company"], "Microsoft")
        self.assertEqual(profile["experience"][0]["title"], "Data Analyst Intern")

        # 6. Validate Project Extractor output
        self.assertTrue(len(profile["project"]) > 0)
        self.assertEqual(profile["project"][0]["name"], "Power BI Sales Dashboard")
        self.assertIn("Excel", profile["project"][0]["tools"])


if __name__ == "__main__":
    unittest.main()