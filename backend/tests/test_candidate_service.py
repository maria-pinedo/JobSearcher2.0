import unittest
import sqlite3
import json
from app.models.database import init_db, DB_PATH
from app.services.candidate_service import save_candidate_profile

class TestCandidateService(unittest.TestCase):
    def setUp(self):
        # Fresh database wipe and initialization before tests run
        init_db()

    def test_save_candidate_profile_integration(self):
        # Simulated payload mirroring your successful ResumeEngine integration test output
        mock_profile = {
            "contact": {"email": "test_maria@email.com", "phone": "123-456-7890"},
            "skills": ["Python", "SQL"],
            "education": [{
                "school": "Appalachian State University",
                "degree": "Master of Science",
                "major": "Applied Data Analytics",
                "graduation_date": "December 2026"
            }],
            "experience": [{
                "title": "Data Analyst Intern",
                "company": "Microsoft",
                "start_date": "May 2025",
                "end_date": "August 2025",
                "responsibilities": ["Developed Power BI dashboards."]
            }],
            "project": [{
                "name": "Sales Tool",
                "tools": ["Power BI", "Excel"],
                "description": ["Tracked revenue metrics."]
            }]
        }

        # Save profile to SQLite database
        candidate_id = save_candidate_profile(mock_profile, candidate_name="Maria Pinedo")
        self.assertIsNotNone(candidate_id)

        # Query database back directly using sqlite3 to confirm correctness
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check Core Candidate Profile Row
        cursor.execute("SELECT name, email, visa_status FROM candidates WHERE id = ?", (candidate_id,))
        cand_row = cursor.fetchone()
        self.assertEqual(cand_row[0], "Maria Pinedo")
        self.assertEqual(cand_row[1], "test_maria@email.com")
        self.assertEqual(cand_row[2], "F-1 STEM OPT")

        # Check Skills Table Mapping
        cursor.execute("SELECT skill_name FROM skills WHERE candidate_id = ?", (candidate_id,))
        skills = [row[0] for row in cursor.fetchall()]
        self.assertIn("Python", skills)
        self.assertIn("SQL", skills)

        # Check Experience Table Mapping and JSON deserialization
        cursor.execute("SELECT company, responsibilities FROM experience WHERE candidate_id = ?", (candidate_id,))
        exp_row = cursor.fetchone()
        self.assertEqual(exp_row[0], "Microsoft")
        resp_list = json.loads(exp_row[1])
        self.assertEqual(resp_list[0], "Developed Power BI dashboards.")

        conn.close()

if __name__ == "__main__":
    unittest.main()