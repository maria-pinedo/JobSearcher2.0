import unittest
from app.services.extractors.project_extractor import ProjectExtractor


class TestProjectExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ProjectExtractor()

    def test_project_extraction(self):
        sample_text = """
        Power BI Sales Dashboard
        Tools: Power BI, SQL, Excel
        • Developed interactive sales dashboards tracking $2M in revenue.
        - Optimized database queries to speed up data loading by 20%.
        """

        results = self.extractor.extract(sample_text)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Power BI Sales Dashboard")
        self.assertIn("Power BI", results[0]["tools"])
        self.assertIn("SQL", results[0]["tools"])
        self.assertEqual(len(results[0]["description"]), 2)
        self.assertEqual(results[0]["description"][0],
                         "Developed interactive sales dashboards tracking $2M in revenue.")


if __name__ == "__main__":
    unittest.main()