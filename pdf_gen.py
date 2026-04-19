from fpdf import FPDF
import datetime

class MaintenanceReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AI Predictive Maintenance Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.datetime.now().strftime("%Y-%m-%%d %H:%M:%S")} | Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(report_text, risk_level, condition):
    pdf = MaintenanceReportPDF()
    pdf.add_page()
    
    # Risk Level Box
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Risk Level: {risk_level}', 1, 1, 'L', fill=True)
    pdf.cell(0, 10, f'Status: {condition}', 1, 1, 'L', fill=True)
    pdf.ln(10)
    
    # Report Content
    pdf.set_font('Arial', '', 11)
    # Filter out emoji characters that Arial might not support
    clean_text = report_text.encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 8, clean_text)
    
    return bytes(pdf.output()) # Return bytes for Streamlit compatibility
