import re


class VisaEligibilityClassifier:
    def __init__(self):
        # Negative keywords: Immediate red flags that disqualify the job
        self.negative_keywords = [
            r"no sponsorship",
            r"must be authorized without sponsorship",
            r"us citizens only",
            r"permanent residents only",
            r"green card required"
        ]

        # Positive keywords: Strong indicators of international student friendliness
        self.positive_keywords = [
            r"stem opt",
            r"opt accepted",
            r"cpt accepted",
            r"visa sponsorship available",
            r"h-1b sponsorship",
            r"h1b sponsorship",
            r"international students welcome"
        ]

    def evaluate(self, job_description):
        """
        Scans a job description for visa-related keywords to determine
        if it is safe for an F-1/OPT student to apply.
        """
        if not job_description:
            return {"visa_score": 0, "reason": "No job description provided"}

        desc_lower = job_description.lower()

        # 1. Check for dealbreakers first (Negative Keywords)
        for neg in self.negative_keywords:
            if re.search(neg, desc_lower):
                return {
                    "visa_score": 0,
                    "reason": f"Disqualified: Contains restrictive phrasing ('{neg}')"
                }

        # 2. Check for explicit green flags (Positive Keywords)
        matched_positives = []
        for pos in self.positive_keywords:
            if re.search(pos, desc_lower):
                matched_positives.append(pos)

        if matched_positives:
            # If explicit positive phrasing is found, score highly
            return {
                "visa_score": 95,
                "reason": f"Highly Compatible: Mentions {', '.join(matched_positives)}"
            }

        # 3. Neutral Ground
        # If the posting doesn't say "no sponsorship" but also doesn't explicitly welcome it,
        # we give it a moderate score. Many companies are open to it but don't state it explicitly.
        return {
            "visa_score": 50,
            "reason": "Neutral: No explicit sponsorship restrictions or guarantees mentioned"
        }