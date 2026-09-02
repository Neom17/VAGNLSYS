import tkinter as tk
from tkinter import Text, END, messagebox
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import html
import os

def create_pdf(data):
   
    file_name = os.path.join(data['save_path'], f"arbetsorder_{data['id']}.pdf")
    
    # A5-format (148.5 x 210 mm)
    c = canvas.Canvas(file_name, pagesize=A5)
    width, height = A5  
    
    margin = 15 * mm
    printable_width = width - (2 * margin)

    # --- TOPPSECTION: Ordernummer & Datum ---
    top_y = height - 20 * mm
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, top_y, f"Order: {data['id']}")

    if 'date' in data and data['date']:
        c.setFont("Helvetica", 10)
        c.drawRightString(width - margin, top_y + 2 * mm, f"Datum: {data['date']}")



    # Svart avdelningslinje
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(margin, top_y - 6 * mm, width - margin, top_y - 6 * mm)

    # --- QR-KOD ---
    #data_dict = {
    #    "order": str(data['id']),
    #    "description": str(data['description'])
    #}
    #qr_data = json.dumps(data_dict, ensure_ascii=False)
    
    qr = QrCodeWidget(data['id'])
    qr_size = 20 * mm  
    qr.barWidth = qr_size
    qr.barHeight = qr_size
    
    d = Drawing(qr_size, qr_size)
    d.add(qr)
    
    qr_x = width - margin - qr_size
    qr_y = top_y - 10 * mm - qr_size
    d.drawOn(c, qr_x, qr_y)

    # --- BESKRIVNING MED AUTOMATISK RADBRYTNING ---
    desc_start_y = top_y - 14 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, desc_start_y, "Beskrivning")

    max_text_width = printable_width - qr_size - 5 * mm
    text_y = desc_start_y - 7 * mm

    styles = getSampleStyleSheet()
    desc_style = ParagraphStyle(
        'DescStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13
    )

    # Skydda specialtecken och hantera radbrytningar säkert
    rensad_text = html.escape(data['description'])
    formaterad_text = rensad_text.replace('\n', '<br/>')
    
    c.save()
    return file_name
    