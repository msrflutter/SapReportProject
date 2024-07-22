from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        self.image('/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/hi.png',10,8,25)
        self.set_font('helvetica','B',20)
        self.cell(80)
        self.cell(30,10,'Title',border=True,ln=1,align='C')
        self.ln(20)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page{self.page_no()}',align='C')

pdf=PDF('P','mm','Letter')
pdf.set_auto_page_break(auto=True,margin=15)#15mm from bottom
pdf.add_page()
pdf.set_font('helvetica','BIU',16)
pdf.set_font('times','',12)
for i in range(1,41):
    pdf.cell(0,10,"Hello world",ln=True) #Entire width of pdf


pdf.output('pdf_2.pdf')