import re
from app.services.extractors.base_extractor import BaseExtractor

class ExperienceExtractor(BaseExtractor):
    def __init__(self):
        # Regular expression to catch common date ranges like "May 2025 - August 2025" or "Jan 2022 - Present"
        self.date_pattern = re.compile(
            r'([A-Za-z]+\s+\d{4})\s*[\-––]\s*([A-Za-z]+\s+\d{4}|Present)',
            re.IGNORECASE
        )

    def extract(self, text):
        """
        Extracts work experience details including job title, company, dates, and responsibilities.
        """
        experiences = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Simple rule-based parser for sequential structural lines
        # In a real resume, text often flows: Title / Company -> Date -> Responsibilities (bullet points)
        current_exp = None

        for i, line in enumerate(lines):
            date_match = self.date_pattern.search(line)

            if date_match:
                # If we hit a new date line, save the previous experience block if it exists
                if current_exp and current_exp["title"]:
                    experiences.append(current_exp)

                start_date, end_date = date_match.groups()

                # Look backward slightly or look at the current line to deduce title/company
                title = "Unknown Title"
                company = "Unknown Company"

                if i > 0 and not self.date_pattern.search(lines[i - 1]):
                    # Inferring that the line right before the date contains the Title/Company
                    info_line = lines[i - 1]
                    parts = re.split(r'[,|\-–]', info_line)
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        company = parts[1].strip()
                    else:
                        title = info_line.strip()

                current_exp = {
                    "title": title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "responsibilities": []
                }
            elif current_exp:
                # If the line starts with a bullet point character, treat it as a responsibility
                if line.startswith(('*', '-', '•')):
                    current_exp["responsibilities"].append(line.lstrip('*•- ').strip())
                # Otherwise, if it's trailing text after the date line, append it safely
                elif len(current_exp["responsibilities"]) < 5:
                    # Fallback to catch loose sentences under an experience block
                    if not any(keyword in line.lower() for keyword in ["education", "skills", "projects"]):
                        current_exp["responsibilities"].append(line)

        # Append the final item if left over
        if current_exp and current_exp["title"]:
            experiences.append(current_exp)

        return experiences