from reportlab.pdfgen import canvas

def generate_pdf(qr_image_path, qr_name, pdf_path):
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, qr_name)
    c.drawImage(qr_image_path, 100, 400, width=300, height=300)
    c.save()
