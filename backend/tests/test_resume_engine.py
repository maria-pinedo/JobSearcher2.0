from app.services.resume_engine import ResumeEngine

sample = """
Maria Jose Pinedo Velarde

maria@email.com

(555) 555-1234

Appalachian State University

Master of Science in Applied Data Analytics

Expected Graduation: December 2026

Python
SQL
Power BI
Forecasting
"""

engine = ResumeEngine()

print(engine.build_profile(sample))