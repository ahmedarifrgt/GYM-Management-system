from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta  # <-- FIXED
import sqlite3
import random
import os

# Constants for styling
GYM_NAME = "ARIF X MAINUL GYM"
GYM_ADDRESS = "SOUTHERN UNVERSITY BANGLADESH"
GYM_PHONE = "01879524393"
LOGO_PATH = "gym_logo.png"  # Replace with actual logo path

def generate_receipt_pdf(member_id, amount, payment_method="Credit Card"):  # <-- FIXED
    # Connect to database and fetch member details
    conn = sqlite3.connect("gym.db")
    cur = conn.cursor()
    cur.execute("SELECT name, phone, membership_type FROM members WHERE id=?", (member_id,))
    member = cur.fetchone()
    conn.close()

    if member:
        name, phone, membership_type = member
    else:
        name, phone, membership_type = "Unknown", "N/A", "N/A"

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"receipt_{member_id}_{timestamp}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['BodyText']
    bold_style = ParagraphStyle('BoldText', parent=normal_style, fontName='Helvetica-Bold')
    footer_style = ParagraphStyle('Footer', parent=normal_style, fontSize=10, textColor=colors.grey)

    # Header section
    if os.path.exists(LOGO_PATH):  # <-- FIXED
        elements.append(Image(LOGO_PATH, width=1.2*inch, height=1.2*inch))
        elements.append(Spacer(1, 12))
    elements.append(Paragraph(GYM_NAME, title_style))
    elements.append(Paragraph(GYM_ADDRESS, normal_style))
    elements.append(Paragraph(f"Phone: {GYM_PHONE}", normal_style))
    elements.append(Spacer(1, 24))

    # Receipt info section
    receipt_number = f"GF-{datetime.now().year}-{random.randint(1, 9999):04d}"
    receipt_date = datetime.now().strftime("%b %d, %Y")
    
    receipt_info = [
        [Paragraph("Receipt No.", normal_style), Paragraph("Date", normal_style)],
        [Paragraph(receipt_number, bold_style), Paragraph(receipt_date, bold_style)]
    ]
    
    receipt_table = Table(receipt_info, colWidths=[3*inch, 3*inch])
    elements.append(receipt_table)
    elements.append(Spacer(1, 24))

    # Divider line
    elements.append(Paragraph("<hr width='100%' color='#667eea'/>", normal_style))
    elements.append(Spacer(1, 12))

    # Title
    elements.append(Paragraph("PAYMENT RECEIPT", subtitle_style))
    elements.append(Spacer(1, 12))

    # Member info
    info_data = [
        ["Member ID:", f"GF-{member_id:04}"],
        ["Name:", name],
        ["Phone:", phone],
        ["Membership:", membership_type]
    ]
    
    member_table = Table(info_data, colWidths=[1.5*inch, 4.5*inch])
    member_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    
    elements.append(member_table)
    elements.append(Spacer(1, 24))

    # Payment section
    elements.append(Paragraph("<hr width='100%' color='#667eea'/>", normal_style))
    payment_data = [
        [Paragraph("Payment Amount:", normal_style), Paragraph(f"${float(amount):.2f}", bold_style)],
        [Paragraph("Payment Method:", normal_style), Paragraph(payment_method, bold_style)]  # <-- FIXED
    ]
    payment_table = Table(payment_data, colWidths=[4*inch, 2*inch])
    payment_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(payment_table)

    # Total row
    total_data = [[Paragraph("Total:", normal_style), Paragraph(f"${float(amount):.2f}", ParagraphStyle('Total', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#667eea')))]]
    total_table = Table(total_data, colWidths=[4*inch, 2*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    
    elements.append(total_table)
    elements.append(Spacer(1, 24))
    
    # Footer section
    elements.append(Paragraph("<hr width='100%' color='#667eea'/>", normal_style))
    
    valid_until = (datetime.now() + timedelta(days=365)).strftime("%b %d, %Y")  # <-- FIXED
    elements.append(Paragraph(f"Thank you for your payment.", normal_style))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Please keep this receipt for your records. Your membership is valid until {valid_until}.", normal_style))
    elements.append(Spacer(1, 48))
    
    elements.append(Paragraph(f"{GYM_NAME} © {datetime.now().year} | Terms & Conditions Apply", footer_style))
    elements.append(Paragraph("Receipt generated automatically", footer_style))

    # Build PDF
    doc.build(elements)
    return filename

# Example usage
# generate_receipt_pdf("1001", "120.00")