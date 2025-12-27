from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from app.models import ReportRequest
from app.services.chart_service import ChartService
import io
import base64
from datetime import datetime

class PdfGenerator:
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='VulnTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.red
        ))

    def _base64_to_image(self, base64_string, width=400, height=300):
        if not base64_string:
            return None
        img_data = base64.b64decode(base64_string)
        img_io = io.BytesIO(img_data)
        return Image(img_io, width=width, height=height)

    def generate_report(self, request: ReportRequest) -> bytes:
        """Generates a PDF report and returns the bytes."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []

        # Title Page
        story.append(Paragraph(f"Security Assessment Report: {request.project_name}", self.styles['ReportTitle']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        story.append(Paragraph(f"Run ID: {request.run_id}", self.styles['Normal']))
        story.append(Spacer(1, 24))

        # Dashboard / Metrics
        story.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        story.append(Paragraph(f"Security Score: {request.metrics.security_score}/100", self.styles['Heading3']))
        
        data = [
            ['Total Vulnerabilities', str(request.metrics.total_vulnerabilities)],
            ['Critical', str(request.metrics.critical_count)],
            ['High', str(request.metrics.high_count)],
            ['Medium', str(request.metrics.medium_count)],
            ['Low', str(request.metrics.low_count)]
        ]
        t = Table(data, colWidths=[200, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 24))

        # Charts
        pie_img = self._base64_to_image(ChartService.generate_severity_pie_chart(request.metrics))
        if pie_img:
            story.append(pie_img)
        
        story.append(PageBreak())

        # Detailed Findings
        story.append(Paragraph("Detailed Findings", self.styles['SectionHeading']))
        for vuln in request.vulnerabilities:
            story.append(Paragraph(f"[{vuln.severity}] {vuln.category}", self.styles['VulnTitle']))
            story.append(Paragraph(f"<b>Affected Component:</b> {vuln.affected_component}", self.styles['Normal']))
            if vuln.line_number:
                story.append(Paragraph(f"<b>Line:</b> {vuln.line_number}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Description:</b> {vuln.description}", self.styles['Normal']))
            if vuln.fix_suggestion:
                story.append(Paragraph(f"<b>Fix Suggestion:</b> {vuln.fix_suggestion}", self.styles['BodyText']))
            story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()
