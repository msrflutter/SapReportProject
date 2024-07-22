import os
from fpdf import FPDF
import google.generativeai as genai

# Configure API key
genai.configure(api_key='AIzaSyBIGfun3ov_HJ6aFYef0hVhglpXcQ1X_Pw')

# Choose a model
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt for generating content
prompt = """
Generate  detailed content for the following activities. Each activity description should exceed a minimum of 1000 words:

1. Activity Description: "The video shows a group of people planting trees in a park, most likely for environmental and community benefits." SDG List: "Life on Land - Goal 15"

2. Activity Description: "The video showcases a rainwater harvesting system in a city environment. It depicts water flowing through a series of small trenches and into a larger reservoir, demonstrating a simple and effective method of collecting and storing rainwater." SDG List: "Clean Water and Sanitation - Goal 6, Climate Action - Goal 13"

3. Activity Description: "Cleaning a fish tank improves the health of the fish living inside by removing waste and debris which can harm their health. This can also reduce the need for medications and other treatments, which can be harmful to the environment." SDG List: "Good Health and Well-being - Goal 3, Life Below Water - Goal 14"

4. Activity Description: "The video depicts a syntropic farming system that uses a variety of plants to create a more sustainable ecosystem and improve soil health. This method is based on global indigenous knowledge and practices that mimic natural ecosystems. The system uses a combination of trees, shrubs, herbs, and other plants to create a diverse and balanced ecosystem. Syntropic farming promotes biodiversity and soil regeneration." SDG List: "Life on Land - Goal 15, Zero Hunger - Goal 2"
"""

# Generate content
response = model.generate_content(prompt)

# Extract and print the generated content (for verification)
generated_content = response.text
print("Generated Content:\n", generated_content)  # Debug print

# Define the report_data
report_data = {
    "title": "Activity Report",
    "content": generated_content
}

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

    def chapter_body(self, body):
        self.set_font('DejaVu', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_content(self, content):
        self.add_page()
        self.chapter_body(content)

pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=15)

# Replace with the actual paths to your font files
pdf.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf", uni=True)
pdf.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf", uni=True)

# Create the PDF
pdf.add_page()
pdf.set_font('DejaVu', 'B', 30)
pdf.cell(0, 10, report_data['title'], 0, 1, 'C')
pdf.ln(20)

# Add the content to the PDF
pdf.add_content(report_data['content'])

pdf.output('Activity_Report.pdf')
