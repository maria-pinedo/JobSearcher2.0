from app.services.extractors.contact_extractor import ContactExtractor
from app.services.extractors.education_extractor import EducationExtractor
from app.services.skill_extractor import SkillExtractor


class ResumeEngine:
    def __init__(self):
        self.extractors = {
            "contact": ContactExtractor(),
            "skills": SkillExtractor(),
            "education": EducationExtractor(),
        }

    def build_profile(self, text: str):
        profile = {}

        for name, extractor in self.extractors.items():
            profile[name] = extractor.extract(text)

        return profile