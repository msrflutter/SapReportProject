from fpdf import FPDF

pdf=FPDF('P','mm','Letter')
pdf.add_page()
pdf.set_font('helvetica','',16)

pdf.cell(40,10,"Hello world",border=True) #width,height
pdf.cell(80,10,"Hello world") #width,height


pdf.output('pdf_1.pdf')