from app.services.extractors.education_extractor import EducationExtractor

sample = """
Appalachian State University

Master of Science in Applied Data Analytics

Expected Graduation: December 2026
"""

extractor = EducationExtractor()

print(extractor.extract(sample))