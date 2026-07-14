import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file
load_dotenv(find_dotenv())

class AdzunaClient:
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        # Base endpoint for US job searches; page 1 is default
        self.base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

        if not self.app_id or not self.app_key:
            raise ValueError("Adzuna API credentials are missing. Check your .env file.")

    def search_jobs(self, query, location="US", limit=10):
        """
        Fetches job postings from Adzuna and normalizes the data structure.
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": limit,
            "what": query,
            "where": location,
            "content-type": "application/json"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            raw_data = response.json()

            return self._normalize_jobs(raw_data.get("results", []))

        except requests.RequestException as e:
            print(f"Error fetching jobs from Adzuna: {e}")
            return []

    def _normalize_jobs(self, raw_jobs):
        """
        Converts Adzuna's specific JSON structure into our application's standard Job format.
        """
        normalized = []
        for job in raw_jobs:
            normalized.append({
                "job_id": str(job.get("id")),
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name", "Unknown Company"),
                "location": job.get("location", {}).get("display_name", "Unknown Location"),
                "description": job.get("description", ""),
                "url": job.get("redirect_url", ""),
                # Grabbing salary info if available, otherwise defaulting to None
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max")
            })
        return normalized