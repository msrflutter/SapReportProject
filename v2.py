import os
from fpdf import FPDF
import google.generativeai as genai

# Configure API key
genai.configure(api_key='AIzaSyBIGfun3ov_HJ6aFYef0hVhglpXcQ1X_Pw')

# Choose a model
model = genai.GenerativeModel('gemini-1.5-flash')

# Improved prompts for generating content
prompts = [
    "Write a half-page description of a video showing people planting trees in a park. Focus on environmental and community benefits. Provide bullet points on how this activity supports SDG Goal 15: Life on Land.",
    "Write a half-page description of a video showcasing a rainwater harvesting system in a city. Emphasize the collection and storage of rainwater. Provide bullet points on how this system supports SDG Goal 6: Clean Water and Sanitation and SDG Goal 13: Climate Action.",
    "Write a half-page description of a video showing the process of cleaning a fish tank. Highlight its importance for fish health and environmental impact. Provide bullet points on how this activity supports SDG Goal 3: Good Health and Well-being and SDG Goal 14: Life Below Water.",
    "Write a half-page description of a video depicting a syntropic farming system. Cover its sustainable practices. Provide bullet points on how this system supports SDG Goal 15: Life on Land and SDG Goal 2: Zero Hunger."
]

# Generate content for each prompt
sections = []
for i in range(0, len(prompts)):
    response = model.generate_content(prompts[i])
    content = response.text.strip()

    # Split the content into description and bullet points
    if "•" in content:
        description, bullet_points = content.split("•", 1)
        bullet_points = ["• " + point.strip() for point in bullet_points.split('\n') if point.strip()]
    else:
        description = content
        bullet_points = []

    sections.append({
        "heading": f"Activity {i + 1}",
        "summary": description.strip(),
        "bullet_points": bullet_points
    })


class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 16)
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

    def bullet_points(self, points):
        self.set_font('DejaVu', '', 12)
        for point in points:
            self.multi_cell(0, 10, point)
        self.ln()

    def add_section(self, heading, summary, bullet_points):
        self.add_page()
        self.chapter_title(heading)
        self.chapter_body(summary)
        self.bullet_points(bullet_points)


pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=15)

# Replace with the actual paths to your font files
pdf.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf", uni=True)
pdf.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf",
             uni=True)

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
    pdf.add_section(section['heading'], section['summary'], section['bullet_points'])

pdf.output('Activity_Report.pdf')
