import os
from fpdf import FPDF
import google.generativeai as genai

# Configure API key
genai.configure(api_key='AIzaSyBIGfun3ov_HJ6aFYef0hVhglpXcQ1X_Pw')

# Choose a model
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompts for generating content
prompts = [
    "Write a detailed description of a video showing a group of people planting trees in a park. The description should focus on environmental and community benefits, and relate it to SDG Goal 15: Life on Land.",
    "Write a detailed description of a video showcasing a rainwater harvesting system in a city. The description should emphasize the collection and storage of rainwater and its relation to SDG Goal 6: Clean Water and Sanitation and Goal 13: Climate Action.",
    "Write a detailed description of a video cleaning a fish tank, highlighting its importance for the health of the fish and its impact on the environment. Relate it to SDG Goal 3: Good Health and Well-being and Goal 14: Life Below Water.",
    "Write a detailed description of a video depicting a syntropic farming system. The description should cover its sustainable practices and its relation to SDG Goal 15: Life on Land and Goal 2: Zero Hunger."
]

# Generate content for each prompt
sections = []
for prompt in prompts:
    response = model.generate_content(prompt)
    section_content = response.text.strip()
    # Truncate content to a reasonable length if necessary (e.g., 250 words)
    section_content = ' '.join(section_content.split()[:500])  # Adjust as needed
    sections.append({
        "heading": prompt.split(':')[0].strip(),
        "content": section_content
    })

class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 20)
        title_w = self.get_string_width(report_data['title']) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(1)
        self.cell(title_w, 10, report_data['title'], border=1, align='C', fill=1, new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, chapter_title):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, chapter_title, new_x="LMARGIN", new_y="NEXT")
        self.ln()

    def chapter_body(self, body):
        self.set_font('DejaVu', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_section(self, heading, content):
        self.add_page()
        self.chapter_title(heading)
        self.chapter_body(content)

pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=10)  # Adjust margin for better text fit

# Replace with the actual paths to your font files
pdf.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf", uni=True)
pdf.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf", uni=True)

# Define the report_data with a title
report_data = {
    "title": "Activity Report"
}

# Create the PDF
pdf.add_page()
pdf.set_font('DejaVu', 'B', 20)
pdf.cell(0, 10, report_data['title'], 0, 1, 'C')
pdf.ln(20)

# Add each section to the PDF
for section in sections:
    pdf.add_section(section['heading'], section['content'])

pdf.output('Activity_Report.pdf')
