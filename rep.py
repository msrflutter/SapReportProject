from fpdf import FPDF

class PDF(FPDF):
    def add_fonts(self):
        try:
            self.add_font("DejaVu", "", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/DejaVuSans.ttf")
            self.add_font("DejaVu", "B", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-bold.ttf")
            self.add_font("DejaVu", "I", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-oblique.ttf")
            self.add_font("DejaVu", "BI", "/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/dejavu-sans-boldoblique.ttf")
        except Exception as e:
            print(f"Error adding fonts: {e}")

pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=15)

# Try adding fonts
pdf.add_fonts()
