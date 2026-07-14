from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Import all of your powerful backend services
from app.services.resume_engine import ResumeEngine
from app.services.job_api_service import AdzunaClient
from app.services.matching_engine import MatchingEngine
from app.services.resume_optimizer import ResumeOptimizer

# Initialize the FastAPI application
app = FastAPI(
    title="JobSearcher2.0 API",
    description="Backend API for Resume Parsing, Job Matching, and AI Optimization",
    version="1.0.0"
)

# Initialize your services (Loaded once when the server starts)
resume_engine = ResumeEngine()
adzuna_client = AdzunaClient()
matching_engine = MatchingEngine()
resume_optimizer = ResumeOptimizer()


# --- Pydantic Models (Define the exact JSON structures the API expects) ---

class ResumeRequest(BaseModel):
    resume_text: str


class JobSearchRequest(BaseModel):
    candidate_profile: Dict[str, Any]
    job_title: str
    location: str = "US"
    limit: int = 5


class OptimizeRequest(BaseModel):
    candidate_profile: Dict[str, Any]
    job_description: str


# --- API Routes ---

@app.get("/")
def health_check():
    """Simple health check to ensure the API is running."""
    return {"status": "ok", "message": "JobSearcher2.0 API is live!"}


@app.post("/api/parse-resume")
def parse_resume(request: ResumeRequest):
    """
    Takes raw resume text and passes it through the ResumeEngine extractors.
    """
    try:
        profile = resume_engine.build_profile(request.resume_text)
        return {"status": "success", "candidate_profile": profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/match-jobs")
def match_jobs(request: JobSearchRequest):
    """
    Searches for live jobs and scores them against the candidate's profile.
    """
    try:
        # 1. Fetch live jobs from Adzuna
        jobs = adzuna_client.search_jobs(
            query=request.job_title,
            location=request.location,
            limit=request.limit
        )

        # 2. Run jobs through the AI Matching Engine & Visa Filter
        matched_jobs = []
        for job in jobs:
            match_result = matching_engine.evaluate_match(request.candidate_profile, job)
            matched_jobs.append(match_result)

        # 3. Sort by the highest match score
        matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)

        return {"status": "success", "matches": matched_jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/optimize-resume")
def optimize_resume(request: OptimizeRequest):
    """
    Uses Google Gemini to recommend ATS improvements based on a specific job.
    """
    try:
        optimization = resume_optimizer.optimize(
            request.candidate_profile,
            request.job_description
        )
        if "error" in optimization:
            raise HTTPException(status_code=400, detail=optimization["error"])

        return {"status": "success", "optimization": optimization}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))