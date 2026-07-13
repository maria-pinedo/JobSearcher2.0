import sqlite3
import json
from app.models.database import DB_PATH


def save_candidate_profile(profile_data, candidate_name="Unknown Candidate", visa_status="F-1 STEM OPT"):
    """
    Takes the structured profile dictionary from ResumeEngine and persists
    it into the SQLite relational database.
    """
    # Extract data blocks from the profile dictionary
    contact = profile_data.get("contact", {})
    skills = profile_data.get("skills", [])
    education_list = profile_data.get("education", [])
    experience_list = profile_data.get("experience", [])
    project_list = profile_data.get("project", [])  # Key is 'project' from ResumeEngine

    # Use contact details for name fallback if available
    email = contact.get("email")
    phone = contact.get("phone")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Start a transaction explicitly
        cursor.execute("BEGIN TRANSACTION;")

        # 1. Insert into candidates table
        cursor.execute("""
            INSERT INTO candidates (name, email, phone, visa_status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                name=excluded.name,
                phone=excluded.phone,
                visa_status=excluded.visa_status
        """, (candidate_name, email, phone, visa_status))

        # Get the id of the candidate (either newly inserted or existing)
        if cursor.lastrowid:
            candidate_id = cursor.lastrowid
        else:
            cursor.execute("SELECT id FROM candidates WHERE email = ?", (email,))
            candidate_id = cursor.fetchone()[0]

        # Clear existing entries for this candidate to prevent duplicates on re-upload
        cursor.execute("DELETE FROM skills WHERE candidate_id = ?", (candidate_id,))
        cursor.execute("DELETE FROM education WHERE candidate_id = ?", (candidate_id,))
        cursor.execute("DELETE FROM experience WHERE candidate_id = ?", (candidate_id,))
        cursor.execute("DELETE FROM projects WHERE candidate_id = ?", (candidate_id,))

        # 2. Insert into skills table
        for skill in skills:
            cursor.execute("""
                INSERT INTO skills (candidate_id, skill_name)
                VALUES (?, ?)
            """, (candidate_id, skill))

        # 3. Insert into education table
        for edu in education_list:
            cursor.execute("""
                INSERT INTO education (candidate_id, school, degree, major, graduation_date)
                VALUES (?, ?, ?, ?, ?)
            """, (candidate_id, edu.get("school"), edu.get("degree"), edu.get("major"), edu.get("graduation_date")))

        # 4. Insert into experience table
        for exp in experience_list:
            # Convert responsibilities list to a JSON string for clean storage
            resp_json = json.dumps(exp.get("responsibilities", []))
            cursor.execute("""
                INSERT INTO experience (candidate_id, title, company, start_date, end_date, responsibilities)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (candidate_id, exp.get("title"), exp.get("company"), exp.get("start_date"), exp.get("end_date"),
                  resp_json))

        # 5. Insert into projects table
        for proj in project_list:
            # Flatten tools list to a comma-separated string as per schema specifications
            tools_str = ", ".join(proj.get("tools", []))
            desc_json = json.dumps(proj.get("description", []))
            cursor.execute("""
                INSERT INTO projects (candidate_id, name, tools, description)
                VALUES (?, ?, ?, ?)
            """, (candidate_id, proj.get("name"), tools_str, desc_json))

        # Commit everything safely if no exceptions occurred
        conn.commit()
        return candidate_id

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Database error encountered: {e}")
        raise e
    finally:
        conn.close()