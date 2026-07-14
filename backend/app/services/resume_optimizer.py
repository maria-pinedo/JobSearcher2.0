import os
import json
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Ensure environment variables are loaded
load_dotenv(find_dotenv())


class ResumeOptimizer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

        # We use gemini-1.5-flash because it is fast, highly capable, and cost-effective
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def optimize(self, candidate_profile, job_description):
        """
        Sends the candidate profile and job description to Gemini to generate
        missing keywords, bullet improvements, and ATS optimization tips.
        """
        if not candidate_profile or not job_description:
            return {"error": "Missing candidate profile or job description"}

        # Define the exact JSON structure we expect the AI to return
        prompt = f"""
        You are an expert AI Career Coach and ATS (Applicant Tracking System) Optimizer.
        Your goal is to compare the candidate's profile to the job description and provide actionable improvements.

        Candidate Profile:
        {json.dumps(candidate_profile, indent=2)}

        Job Description:
        {job_description}

        Return ONLY a valid JSON object with the exact following structure. Do not include markdown formatting like ```json.
        {{
            "missing_keywords": ["keyword1", "keyword2"],
            "bullet_improvements": [
                {{
                    "original": "Old bullet from candidate experience",
                    "improved": "New ATS-optimized bullet incorporating job keywords and action verbs"
                }}
            ],
            "ats_score": 85,
            "skill_gaps": ["Brief explanation of missing skills"]
        }}
        """

        try:
            # Force the model to output strict JSON
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )

            # Parse the JSON string returned by Gemini into a Python dictionary
            return json.loads(response.text)

        except Exception as e:
            print(f"Error generating optimization with Gemini: {e}")
            return None