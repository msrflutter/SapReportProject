from fpdf import FPDF

report_data = {
    "title": "Environmental Management System (EMS)",
    "sections": [
        {
            "heading": "3.0 Environmental",
            "content": "Environmental management system (EMS)\nThe Company manages the environmental elements of its operations through a global environmental management system (EMS) that covers the Company’s worldwide product design, development, and manufacturing operations (including distribution, fulfillment, and internal repair operations) for computer products and devices, data center products, mobile devices, smart devices, accessories, and converged network equipment. The scope encompasses these same activities when performed by its subsidiary and/or affiliate companies."
        },
        {
            "heading": "ISO 14001:2015 Certification",
            "content": "All of the Company’s sites in the EMS scope are ISO 14001:2015 certified. See here to view the Company’s Global ISO 14001:2015 certificates.\n\nThe Company has established, implemented, and maintained an Environmental Affairs Policy which can be viewed here."
        },
        {
            "heading": "Significant Environmental Aspect (SEA) Evaluation",
            "content": "Within the framework of the Company’s EMS, it annually conducts a Significant Environmental Aspect (SEA) evaluation process where it identifies and evaluates the aspects of its operations that have actual or potential significant impacts on the environment using a methodology that includes input from the Company’s Enterprise Risk Management (ERM) process. Metrics and controls are established for these significant environmental aspects. Performance relative to these metrics is tracked and reported. Performance targets are established for select environmental aspects annually with considerations including Environmental Affairs Policy, regulatory requirements, customer requirements, stakeholder input, environmental and financial impact, and management directives."
        },
        {
            "heading": "Significant Environmental Aspects (FY 2023/24)",
            "content": "During FY 2023/24, the Company’s significant environmental aspects included:\n• Product materials – including use of recycled plastics and environmentally preferable materials where possible\n• Product packaging\n• Product energy consumption and emissions\n• Product end-of-life management\n• Site air emissions, specifically greenhouse gas (GHG) emissions\n• Site energy consumption\n• Supplier environmental performance\n• Product transportation\n• Waste management\n• Water management\n• Impact of Lenovo’s net-zero commitment"
        },
        {
            "heading": "Objective and Performance Targets",
            "content": "Objective and performance targets were established for the aspects listed above. The Company’s performance against these objectives and targets is available in Section 8.0.\n\nThe Company’s energy, GHG emissions (Scope 1 and 2), waste, and water data are externally verified to a reasonable level of assurance. The Company’s GHG emissions (Scope 3) data is externally verified to a limited level of assurance. The FY 2023/24 Verification Statements for GHG, Energy, Waste and Water can be viewed here."
        },
        {
            "heading": "Lenovo ESG Navigator",
            "content": "The Company has developed and tested an innovative ESG data management system called Lenovo ESG Navigator that helps monitor key ESG metrics and deliver near-real-time insights. In FY 2023/24, the Company deployed Lenovo ESG Navigator at two manufacturing sites in China – the Company’s Lenovo South Smart Campus and Tianjin Smart Campus facilities – where it is being used to collect and monitor environmental data, including energy, greenhouse gas emissions, water, and waste data. In addition, Lenovo ESG Navigator is in use at the Company’s Beijing Headquarters where it is deployed as a smart building solution and within the Company’s Global Supply Chain where it collects and monitors select ESG data related to suppliers and products.\n\nAs next steps, it plans to continue to coach users at the facilities where it has been deployed on Lenovo ESG Navigator’s effective use and will continue to rollout the platform to additional manufacturing sites beginning with its facility in Monterrey, Mexico. The Company anticipates the tool to have many benefits including: driving progress toward the Company’s net-zero emissions target and other environmental targets, reducing manual workload related to data collection and reporting, improving data accuracy, providing near-real-time tracking and analysis of environmental KPIs, centralizing ESG data and documents, and facilitating ESG knowledge sharing. At the sites where Lenovo ESG Navigator has been deployed, the environmental focal points are using the system to provide the data input into the Company’s internal environmental database."
        }
    ]
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

    def chapter_title(self, chapter_title):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, chapter_title, new_x="LMARGIN", new_y="NEXT")
        self.ln()

    def chapter_body(self, body):
        self.set_font('DejaVu', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, heading, content, images=None, img1_size=(85, 85), img2_size=(15, 15)):
        self.add_page()
        self.chapter_title(heading)
        self.chapter_body(content)
        if images:
            self.add_images(images, img1_size, img2_size)

    def add_images(self, images, img1_size, img2_size):
        img1_width, img1_height = img1_size
        img2_width, img2_height = img2_size
        spacing = 10
        total_width = img1_width + img2_width + spacing
        x_offset = (self.w - total_width) / 2
        y_offset = self.get_y()

        self.image(images[0], x=x_offset, y=y_offset, w=img1_width, h=img1_height)
        self.image(images[1], x=x_offset + img1_width + spacing, y=y_offset, w=img2_width, h=img2_height)
        self.ln(max(img1_height, img2_height) + 10)  # Adjust the line height based on the maximum height of the images


pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=15)

# Replace with the actual paths to your font files
pdf.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf", uni=True)
pdf.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf",
             uni=True)

pdf.add_page()

for section in report_data['sections']:
    if section['heading'] == "ISO 14001:2015 Certification":
        images = [
            "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/E-WEB-Goal-13.png",
            "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/z685udbnknga1.jpg"
        ]
        pdf.add_chapter(section['heading'], section['content'], images=images, img1_size=(100, 100),
                        img2_size=(15, 15))  # Adjust sizes as needed
    else:
        pdf.add_chapter(section['heading'], section['content'])

pdf.output('Environmental_Management_System_Report.pdf')
