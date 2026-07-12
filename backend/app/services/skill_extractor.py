import json
from pathlib import Path

from app.services.extractors.base_extractor import BaseExtractor


class SkillExtractor(BaseExtractor):
    def __init__(self):
        skills_file = Path(__file__).parent.parent / "data" / "skills.json"

        with open(skills_file, "r", encoding="utf-8") as f:
            self.skills = json.load(f)

    def extract(self, text: str):
        text_lower = text.lower()

        found = []

        for skill in self.skills:
            if skill.lower() in text_lower:
                found.append(skill)

        return sorted(set(found))