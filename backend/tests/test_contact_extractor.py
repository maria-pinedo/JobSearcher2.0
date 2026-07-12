from app.services.extractors.contact_extractor import ContactExtractor

sample = """
Maria Jose Pinedo Velarde

maria@email.com

(555) 555-1234
"""

extractor = ContactExtractor()
print(extractor.extract(sample))