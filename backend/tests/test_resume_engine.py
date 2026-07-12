from app.services.resume_engine import ResumeEngine

sample = """
Maria Jose Pinedo Velarde

maria@email.com

(555) 555-1234

Python
SQL
Power BI
Forecasting
"""

engine = ResumeEngine()

print(engine.build_profile(sample))