import json
import re
from pathlib import Path

from app.services.extractors.base_extractor import BaseExtractor


class EducationExtractor(BaseExtractor):

    def __init__(self):
        degrees_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "degrees.json"
        )

        with open(degrees_file, "r", encoding="utf-8") as f:
            self.degrees = json.load(f)

    def extract(self, text: str):

        education = []

        degree_found = None

        for degree in self.degrees:
            if degree.lower() in text.lower():
                degree_found = degree
                break

        school = None

        school_pattern = (
            r"([A-Z][A-Za-z&.\- ]+"
            r"(University|College|Institute|School))"
        )

        school_match = re.search(school_pattern, text)

        if school_match:
            school = school_match.group()

        major = None

        if degree_found:
            pattern = degree_found + r"\s+(?:in\s+)?([A-Za-z &]+)"

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                major = match.group(1).strip()

        graduation = None

        grad_match = re.search(
            r"(Expected Graduation|Graduation|Graduated):?\s*(.*)",
            text,
            re.IGNORECASE,
        )

        if grad_match:
            graduation = grad_match.group(2).strip()

        education.append(
            {
                "school": school,
                "degree": degree_found,
                "major": major,
                "graduation_date": graduation,
            }
        )

        return education