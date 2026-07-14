import re
from sentence_transformers import SentenceTransformer, util
from app.services.visa_classifier import VisaEligibilityClassifier


class MatchingEngine:
    def __init__(self):
        # Load the pre-trained NLP model
        self.nlp_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Initialize the gatekeeper
        self.visa_classifier = VisaEligibilityClassifier()

    def calculate_keyword_match(self, candidate_skills, job_description):
        """
        Calculates a baseline Match Score checking if candidate skills
        exist within the job description text.
        """
        if not candidate_skills or not job_description:
            return 0.0

        skills_clean = set(skill.lower() for skill in candidate_skills)
        job_desc_lower = job_description.lower()

        matched_skills = [skill for skill in skills_clean if skill in job_desc_lower]

        if not skills_clean:
            return 0.0

        score = (len(matched_skills) / len(skills_clean)) * 100
        return round(score, 2)

    def calculate_semantic_match(self, candidate_skills, job_description):
        """
        Uses NLP embeddings to calculate the contextual similarity (Cosine Similarity)
        between the candidate's skill profile and the job description.
        """
        if not candidate_skills or not job_description:
            return 0.0

        # Convert the list of skills into a single contextual phrase
        candidate_text = "Candidate expertise: " + ", ".join(candidate_skills)

        # Generate high-dimensional vectors (embeddings)
        candidate_embedding = self.nlp_model.encode(candidate_text)
        job_embedding = self.nlp_model.encode(job_description)

        # Calculate Cosine Similarity
        similarity = util.cos_sim(candidate_embedding, job_embedding).item()

        # Convert to percentage and cap at 100
        score = max(0.0, min(similarity * 100, 100.0))
        return round(score, 2)

    def evaluate_match(self, candidate_profile, job_posting):
        """
        Main pipeline to evaluate a job against a candidate.
        Returns a blended score using strict keywords, NLP semantics, and Visa eligibility.
        """
        candidate_skills = candidate_profile.get("skills", [])
        job_desc = job_posting.get("description", "")

        keyword_score = self.calculate_keyword_match(candidate_skills, job_desc)
        semantic_score = self.calculate_semantic_match(candidate_skills, job_desc)

        # Blended Score: 40% Keyword Accuracy, 60% Semantic Understanding
        blended_score = round((keyword_score * 0.4) + (semantic_score * 0.6), 2)

        # Run the Visa Compatibility Filter
        visa_evaluation = self.visa_classifier.evaluate(job_desc)

        return {
            "job_id": job_posting.get("job_id"),
            "job_title": job_posting.get("title"),
            "company": job_posting.get("company"),
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "match_score": blended_score,
            "scoring_method": "blended_nlp",
            "visa_score": visa_evaluation["visa_score"],
            "visa_reason": visa_evaluation["reason"]
        }