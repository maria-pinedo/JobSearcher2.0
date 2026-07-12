from app.services.extractors.contact_extractor import ContactExtractor
from app.services.skill_extractor import SkillExtractor


class ResumeEngine:

    def __init__(self):
        self.contact = ContactExtractor()
        self.skills = SkillExtractor()

    def build_profile(self, text: str):
        return {
            "contact": self.contact.extract(text),
            "skills": self.skills.extract(text)
        }