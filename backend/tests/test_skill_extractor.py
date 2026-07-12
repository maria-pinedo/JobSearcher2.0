from app.services.skill_extractor import SkillExtractor

sample_resume = """
Python
SQL
Power BI
Machine Learning
Forecasting
Excel
"""

extractor = SkillExtractor()

print(extractor.extract(sample_resume))