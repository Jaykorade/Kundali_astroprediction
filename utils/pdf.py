from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(filename, kundali, dasha):
    c = canvas.Canvas(filename, pagesize=letter)

    c.drawString(50, 750, "Kundali Report")

    y = 700
    for k, v in kundali["planets"].items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 20

    y -= 20
    c.drawString(50, y, "Dasha:")

    y -= 20
    for d in dasha:
        c.drawString(50, y, f"{d['planet']} {d['start']} - {d['end']}")
        y -= 20

    c.save()