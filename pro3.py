from fpdf import FPDF

title='X'
class PDF(FPDF):
    def header(self):
        self.image('/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/hi.png',10,8,25)
        self.set_font('helvetica','B',20)
        title_w=self.get_string_width(title)+6
        doc_w=self.w
        self.set_x((doc_w-title_w)/2)
        self.set_draw_color(0,80,180)
        self.set_fill_color(230,230,0)
        self.set_text_color(220,50,50)
        self.set_line_width(1)
        self.cell(title_w,10,title,border=1,ln=1,align='C',fill=1)
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page{self.page_no()}',align='C')

    def chapter(self,name):
        with open(name,'rb') as fh:
            txt=fh.read().decode('latin-1')
        self.set_font('times','',12)
        self.multi_cell(0,5,txt)
        self.ln()
pdf=PDF('P','mm','Letter')
pdf.set_auto_page_break(auto=True,margin=15)#15mm from bottom
pdf.add_page()
pdf.chapter('/Users/amogh1/PycharmProjects/pythonProject/pdfcreate/nahhh.rtf')

pdf.output('pdf_3.pdf')