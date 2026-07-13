import re
from app.services.extractors.base_extractor import BaseExtractor


class ProjectExtractor(BaseExtractor):
    def __init__(self):
        # Pattern to specifically grab explicit tool listings like "Tools: Python, SQL"
        self.tools_pattern = re.compile(r'(?:tools|technologies|stack)\s*:\s*(.*)', re.IGNORECASE)

    def extract(self, text):
        """
        Extracts personal or academic projects, including project name, tools used, and descriptions.
        """
        projects = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        current_project = None

        for i, line in enumerate(lines):
            tools_match = self.tools_pattern.search(line)

            if tools_match:
                # If we encounter a "Tools:" line, the line right before it is usually the Project Name
                project_name = "Unknown Project"
                if i > 0:
                    project_name = lines[i - 1].strip()

                # If a project block was already open, save it before opening a new one
                if current_project:
                    projects.append(current_project)

                # Split tools by commas or spaces
                tools_list = [t.strip() for t in re.split(r'[,|]', tools_match.group(1)) if t.strip()]

                current_project = {
                    "name": project_name,
                    "tools": tools_list,
                    "description": []
                }
            elif current_project:
                # Append descriptive bullets or notes following the tool classification
                if line.startswith(('*', '-', '•')):
                    current_project["description"].append(line.lstrip('*•- ').strip())
                elif len(current_project["description"]) < 4:
                    # Guardrail to stop capturing if we hit unrelated major sections
                    if any(keyword in line.lower() for keyword in
                           ["education", "experience", "skills", "certifications"]):
                        projects.append(current_project)
                        current_project = None
                    else:
                        current_project["description"].append(line)

        if current_project:
            projects.append(current_project)

        return projects