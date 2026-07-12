import re
from app.services.extractors.base_extractor import BaseExtractor


class ContactExtractor(BaseExtractor):

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_PATTERN = (
        r"(?:\+?1[\s.-]?)?"
        r"(?:\(?\d{3}\)?[\s.-]?)"
        r"\d{3}[\s.-]?\d{4}"
    )

    def extract(self, text: str):
        email = None
        phone = None

        email_match = re.search(self.EMAIL_PATTERN, text)
        if email_match:
            email = email_match.group()

        phone_match = re.search(self.PHONE_PATTERN, text)
        if phone_match:
            phone = phone_match.group()

        return {
            "email": email,
            "phone": phone
        }