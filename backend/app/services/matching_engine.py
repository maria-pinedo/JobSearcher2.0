import re


class MatchingEngine:
    def __init__(self):
        # We leave a placeholder here for the future NLP model
        self.nlp_model = None

    def calculate_keyword_match(self, candidate_skills, job_description):
        """
        Calculates a baseline Match Score checking if candidate skills
        exist within the job description text.
        """
        if not candidate_skills or not job_description:
            return 0.0

        # Normalize skills to lowercase for case-insensitive matching
        skills_clean = set(skill.lower() for skill in candidate_skills)
        job_desc_lower = job_description.lower()

        matched_skills = []
        for skill in skills_clean:
            # Check if the exact skill phrase exists in the job description
            if skill in job_desc_lower:
                matched_skills.append(skill)

        # Calculate percentage: (Matched Skills / Total Candidate Skills) * 100
        score = (len(matched_skills) / len(skills_clean)) * 100

        return round(score, 2)

    def evaluate_match(self, candidate_profile, job_posting):
        """
        Main pipeline to evaluate a job against a candidate.
        Returns a detailed dictionary of the match results.
        """
        candidate_skills = candidate_profile.get("skills", [])
        job_desc = job_posting.get("description", "")

        keyword_score = self.calculate_keyword_match(candidate_skills, job_desc)

        return {
            "job_id": job_posting.get("job_id"),
            "job_title": job_posting.get("title"),
            "company": job_posting.get("company"),
            "match_score": keyword_score,
            "scoring_method": "keyword_baseline"
        }