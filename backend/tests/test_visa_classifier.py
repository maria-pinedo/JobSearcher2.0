import unittest
from app.services.visa_classifier import VisaEligibilityClassifier


class TestVisaClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = VisaEligibilityClassifier()

    def test_negative_match(self):
        job_desc = "Looking for a Data Analyst. Candidates must be authorized without sponsorship. US Citizens only."
        result = self.classifier.evaluate(job_desc)

        self.assertEqual(result["visa_score"], 0)
        self.assertIn("Disqualified", result["reason"])

    def test_positive_match(self):
        job_desc = "We are hiring! STEM OPT and H-1B sponsorship available for qualified candidates."
        result = self.classifier.evaluate(job_desc)

        self.assertEqual(result["visa_score"], 95)
        self.assertIn("Highly Compatible", result["reason"])
        self.assertIn("stem opt", result["reason"])

    def test_neutral_match(self):
        job_desc = "Seeking a backend developer proficient in Python and SQL."
        result = self.classifier.evaluate(job_desc)

        self.assertEqual(result["visa_score"], 50)
        self.assertIn("Neutral", result["reason"])


if __name__ == "__main__":
    unittest.main()