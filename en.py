from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, storage, db
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, Image
import datetime

# Initialize Flask app
app = Flask(__name__)

# Firebase configuration


# Configure Google Generative AI API


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

# Define the PDFGenerator class using ReportLab
class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(self.filename, pagesize=letter)
        self.elements = []
        self.styles = getSampleStyleSheet()

        # Register custom fonts
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics

        pdfmetrics.registerFont(TTFont('DejaVuSans', '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Italic', '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-BoldItalic', '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf'))

    def add_title(self, title):
        title_style = self.styles['Title']
        title_style.fontName = 'DejaVuSans-Bold'
        title_paragraph = Paragraph(title, title_style)
        self.elements.append(title_paragraph)
        self.elements.append(Spacer(1, 12))

    def add_section(self, heading, summary, bullet_points, sdgs):
        heading_style = self.styles['Heading1']
        heading_style.fontName = 'DejaVuSans-Bold'
        heading_paragraph = Paragraph(heading, heading_style)
        self.elements.append(heading_paragraph)

        summary_style = self.styles['BodyText']
        summary_style.fontName = 'DejaVuSans'
        summary_paragraph = Paragraph(summary, summary_style)
        self.elements.append(summary_paragraph)

        if bullet_points:
            list_style = ParagraphStyle(name='BulletList', bulletFontSize=10, bulletIndent=10, leftIndent=20, spaceBefore=12, spaceAfter=12, fontName='DejaVuSans')
            bullet_list = ListFlowable([Paragraph(bp, list_style) for bp in bullet_points], bulletType='bullet')
            self.elements.append(bullet_list)

        self.add_images(sdgs)
        self.elements.append(Spacer(1, 24))

    def add_images(self, sdgs):
        image_added = set()
        for sdg in sdgs:
            sdg_key = sdg.split(':')[0].strip()  # Extract "Goal X"
            description = self.get_sdg_description(sdg_key)
            if sdg_key in sdg_images and sdg_images[sdg_key] not in image_added:
                img_path = sdg_images[sdg_key]
                if os.path.exists(img_path):
                    img = Image(img_path, width=1.5*inch, height=1.5*inch)
                    self.elements.append(img)
                    self.elements.append(Spacer(1, 6))
                    description_paragraph = Paragraph(description, self.styles['BodyText'])
                    description_paragraph.fontName = 'DejaVuSans'
                    self.elements.append(description_paragraph)
                    self.elements.append(Spacer(1, 12))
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

    def build_pdf(self):
        self.doc.build(self.elements)

# API endpoint to generate PDF
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        prompts = data.get("prompts", [])

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
                print(f"Error generating content for prompt '{prompt['description']}']: {e}")

        # Create PDF and upload to Firebase
        pdf_gen = PDFGenerator('image_Report.pdf')
        pdf_gen.add_title("Activity Report")

        for section in sections:
            pdf_gen.add_section(section['heading'], section['summary'], section['bullet_points'], section['sdgs'])

        pdf_gen.build_pdf()

        # Upload PDF to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(os.path.basename(pdf_gen.filename))
        blob.upload_from_filename(pdf_gen.filename)

        # Generate a signed URL for the PDF file
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # URL expires in 1 hour
        signed_url = blob.generate_signed_url(expiration_time, method='GET')

        # Save Metadata in Firebase Realtime Database
        report_data = {
            "title": "Activity Report",
            "url": signed_url,
            "sections": sections
        }

        ref = db.reference('py/')
        ref.push(report_data)

        return jsonify({
            "message": "PDF uploaded and metadata saved to Firebase successfully.",
            "signed_url": signed_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
