import os
from fpdf import FPDF
import google.generativeai as genai

# Configure API key
genai.configure(api_key='AIzaSyBIGfun3ov_HJ6aFYef0hVhglpXcQ1X_Pw')

# Choose a model
model = genai.GenerativeModel('gemini-1.5-flash')

# Improved prompts with SDG descriptions
prompts = [
    {
        "description": (
            "Write a half-page description of a video showing people planting trees in a park. "
            "Focus on environmental and community benefits. "
            "Include information on how this activity aligns with SDG 15: Life on Land, "
            "which aims to protect, restore, and promote sustainable use of terrestrial ecosystems."
        ),
        "sdgs": ["Goal 15: Life on Land"]
    },
    {
        "description": (
            "Write a half-page description of a video showcasing a rainwater harvesting system in a city. "
            "Emphasize the collection and storage of rainwater. "
            "Include information on how this system supports SDG 6: Clean Water and Sanitation, "
            "which aims to ensure availability and sustainable management of water and sanitation for all, "
            "and SDG 13: Climate Action, which aims to take urgent action to combat climate change and its impacts."
        ),
        "sdgs": ["Goal 6: Clean Water and Sanitation", "Goal 13: Climate Action"]
    },
    {
        "description": (
            "Write a half-page description of a video showing the process of cleaning a fish tank. "
            "Highlight its importance for fish health and environmental impact. "
            "Include information on how proper tank maintenance relates to SDG 3: Good Health and Well-being, "
            "which aims to ensure healthy lives and promote well-being for all, and SDG 14: Life Below Water, "
            "which aims to conserve and sustainably use the oceans, seas, and marine resources."
        ),
        "sdgs": ["Goal 3: Good Health and Well-being", "Goal 14: Life Below Water"]
    },
    {
        "description": (
            "Write a half-page description of a video depicting a syntropic farming system. "
            "Cover its sustainable practices. "
            "Include information on how syntropic farming supports SDG 15: Life on Land, "
            "which aims to protect, restore, and promote sustainable use of terrestrial ecosystems, "
            "and SDG 2: Zero Hunger, which aims to end hunger, achieve food security and improved nutrition, and promote sustainable agriculture."
        ),
        "sdgs": ["Goal 15: Life on Land", "Goal 2: Zero Hunger"]
    }
]

# Generate content for each prompt
sections = []
for prompt in prompts:
    try:
        response = model.generate_content(prompt["description"])
        content = response.text.strip()
        print(f"Response for prompt '{prompt['description']}': {content}")

        # Split the content into description and bullet points
        if "•" in content:
            description, bullet_points = content.split("•", 1)
            bullet_points = ["• " + point.strip() for point in bullet_points.split('\n') if point.strip()]
        else:
            description = content
            bullet_points = []

        sections.append({
            "heading": f"Activity {len(sections) + 1}",
            "summary": description.strip(),
            "bullet_points": bullet_points,
            "sdgs": prompt["sdgs"]
        })
    except Exception as e:
        print(f"Error generating content for prompt '{prompt['description']}': {e}")

# Mapping of SDG goals to image file paths
sdg_images = {
    "Goal 1": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/1.png",
    "Goal 2": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/2.png",
    "Goal 3": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/3.png",
    "Goal 4": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/4.png",
    "Goal 5": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/5.png",
    "Goal 6": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/6.png",
    "Goal 7": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/7.png",
    "Goal 8": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/8.png",
    "Goal 9": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/9.png",
    "Goal 10": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/10.png",
    "Goal 11": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/11.png",
    "Goal 12": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/12.png",
    "Goal 13": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/13.png",
    "Goal 14": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/14.png",
    "Goal 15": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/15.png",
    "Goal 16": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/16.png",
    "Goal 17": "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/17.png"
}

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

    def add_images(self, sdgs):
        image_added = set()
        for sdg in sdgs:
            # Normalize the SDG goal string
            sdg_key = sdg.split(':')[0].strip()  # Extract "Goal X"
            description = self.get_sdg_description(sdg_key)
            if sdg_key in sdg_images and sdg_images[sdg_key] not in image_added:
                img_path = sdg_images[sdg_key]
                if os.path.exists(img_path):
                    self.image(img_path, x=10, w=30)  # Adjust x position and size as needed
                    self.ln(10)  # Adjust line height as needed
                    self.set_font('DejaVu', '', 10)
                    self.multi_cell(0, 10, description)
                    self.ln(5)  # Add space between image and description
                    image_added.add(img_path)
                else:
                    print(f"Image {img_path} not found.")
            else:
                print(f"SDG {sdg_key} not in image mapping.")

    def get_sdg_description(self, sdg_key):
        descriptions = {
            "Goal 1": "SDG 1: No Poverty - End poverty in all its forms everywhere.",
            "Goal 2": "SDG 2: Zero Hunger - End hunger, achieve food security and improved nutrition, and promote sustainable agriculture.",
            "Goal 3": "SDG 3: Good Health and Well-being - Ensure healthy lives and promote well-being for all at all ages.",
            "Goal 4": "SDG 4: Quality Education - Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.",
            "Goal 5": "SDG 5: Gender Equality - Achieve gender equality and empower all women and girls.",
            "Goal 6": "SDG 6: Clean Water and Sanitation - Ensure availability and sustainable management of water and sanitation for all.",
            "Goal 7": "SDG 7: Affordable and Clean Energy - Ensure access to affordable, reliable, sustainable, and modern energy for all.",
            "Goal 8": "SDG 8: Decent Work and Economic Growth - Promote sustained, inclusive, and sustainable economic growth, full and productive employment, and decent work for all.",
            "Goal 9": "SDG 9: Industry, Innovation, and Infrastructure - Build resilient infrastructure, promote inclusive and sustainable industrialization, and foster innovation.",
            "Goal 10": "SDG 10: Reduced Inequalities - Reduce inequality within and among countries.",
            "Goal 11": "SDG 11: Sustainable Cities and Communities - Make cities and human settlements inclusive, safe, resilient, and sustainable.",
            "Goal 12": "SDG 12: Responsible Consumption and Production - Ensure sustainable consumption and production patterns.",
            "Goal 13": "SDG 13: Climate Action - Take urgent action to combat climate change and its impacts.",
            "Goal 14": "SDG 14: Life Below Water - Conserve and sustainably use the oceans, seas, and marine resources for sustainable development.",
            "Goal 15": "SDG 15: Life on Land - Protect, restore, and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss.",
            "Goal 16": "SDG 16: Peace, Justice, and Strong Institutions - Promote peaceful and inclusive societies for sustainable development, provide access to justice for all, and build effective, accountable, and inclusive institutions at all levels.",
            "Goal 17": "SDG 17: Partnerships for the Goals - Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development."
        }
        return descriptions.get(sdg_key, "Description not available.")

    def add_section(self, heading, summary, bullet_points, sdgs):
        self.add_page()
        self.chapter_title(heading)
        self.chapter_body(summary)
        self.bullet_points(bullet_points)
        self.add_images(sdgs)

pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=15)

# Replace with the actual paths to your font files
pdf.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf")
pdf.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf")
pdf.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf")

# Define the report_data with a title
report_data = {
    "title": "Activity Report"
}

# Create the PDF
pdf.add_page()
pdf.set_font('DejaVu', 'B', 20)
pdf.cell(0, 10, report_data['title'], new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(20)

# Add each section to the PDF
for section in sections:
    pdf.add_section(section['heading'], section['summary'], section['bullet_points'], section['sdgs'])

pdf.output('image_Report.pdf')
