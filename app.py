from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, storage, db
import os
from fpdf import FPDF
import google.generativeai as genai
import datetime

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/saphackproject-firebase-adminsdk-za5qq-4a5b2c9d60.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://saphackproject-default-rtdb.firebaseio.com/',
    'storageBucket': 'saphackproject.appspot.com'
})

# Configure Google Generative AI API
genai.configure(api_key='AIzaSyBNd9o9WTvrPsh9QIcNx3SKtaspghfJBW8')
model = genai.GenerativeModel('gemini-1.5-flash')

# Improved prompts with SDG descriptions
prompts = [
    # Define your prompts here...
]

# Mapping of SDG goals to image file paths
sdg_images = {
    # Map SDG goals to image paths here...
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
        self.cell(title_w, 10, report_data['title'], border=1, align='C', fill=1)
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
            sdg_key = sdg.split(':')[0].strip()
            description = self.get_sdg_description(sdg_key)
            if sdg_key in sdg_images and sdg_images[sdg_key] not in image_added:
                img_path = sdg_images[sdg_key]
                if os.path.exists(img_path):
                    img_width = 30
                    img_x = (self.w - img_width) / 2
                    self.image(img_path, x=img_x, w=img_width)
                    self.ln(10)
                    self.set_font('DejaVu', '', 10)
                    self.multi_cell(0, 10, description)
                    self.ln(5)
                    image_added.add(img_path)
                else:
                    print(f"Image {img_path} not found.")
            else:
                print(f"SDG {sdg_key} not in image mapping.")

    def get_sdg_description(self, sdg_key):
        descriptions = {
            # Define SDG descriptions here...
        }
        return descriptions.get(sdg_key, "Description not available.")

    def add_section(self, heading, summary, bullet_points, sdgs):
        self.add_page()
        self.chapter_title(heading)
        self.chapter_body(summary)
        self.bullet_points(bullet_points)
        self.add_images(sdgs)

@app.route('/generate-pdf', methods=['GET'])
def generate_pdf():
    try:
        # Generate PDF
        pdf_file_path = '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/generated_report.pdf'
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

        pdf.add_page()
        pdf.set_font('DejaVu', 'B', 20)
        pdf.cell(0, 10, report_data['title'], new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(20)

        # Generate content for each prompt
        sections = []
        for prompt in prompts:
            try:
                response = model.generate_content(prompt["description"])
                content = response.text.strip()
                print(f"Response for prompt '{prompt['description']}': {content}")

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

        # Add each section to the PDF
        for section in sections:
            pdf.add_section(section['heading'], section['summary'], section['bullet_points'], section['sdgs'])

        # Save PDF locally
        pdf.output(pdf_file_path)

        # Upload PDF to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(os.path.basename(pdf_file_path))
        blob.upload_from_filename(pdf_file_path)

        # Generate a signed URL for the PDF file
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        signed_url = blob.generate_signed_url(expiration_time, method='GET')

        # Save Metadata in Firebase Realtime Database
        metadata = {
            "title": "Activity Report",
            "url": signed_url,
            "sections": sections
        }

        ref = db.reference('pdf_reports/')
        ref.push(metadata)

        return jsonify({"message": "PDF generated and uploaded successfully", "url": signed_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
