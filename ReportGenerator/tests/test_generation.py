import unittest
from app.models import ReportRequest, Vulnerability, ScanMetrics
from app.services.html_generator import HtmlGenerator
from app.services.chart_service import ChartService
from app.services.pdf_generator import PdfGenerator
import os

class TestReportGeneration(unittest.TestCase):
    def setUp(self):
        self.metrics = ScanMetrics(
            total_vulnerabilities=10,
            critical_count=2,
            high_count=3,
            medium_count=4,
            low_count=1,
            security_score=65.5
        )
        self.vulns = [
            Vulnerability(
                id="VULN-001", severity="CRITICAL", category="Injection",
                description="SQL Injection", affected_component="Login",
                line_number=10, fix_suggestion="Use prepared statements"
            ),
             Vulnerability(
                id="VULN-002", severity="HIGH", category="XSS",
                description="Reflected XSS", affected_component="Search",
                line_number=20, fix_suggestion="Escape output"
            )
        ]
        self.request = ReportRequest(
            run_id="RUN-123",
            report_type="technical",
            format="html",
            vulnerabilities=self.vulns,
            metrics=self.metrics,
            project_name="Test Project"
        )
        self.html_gen = HtmlGenerator()
        self.pdf_gen = PdfGenerator()

    def test_chart_generation(self):
        pie = ChartService.generate_severity_pie_chart(self.metrics)
        self.assertTrue(len(pie) > 0)
        
    def test_html_generation(self):
        html = self.html_gen.generate_report(self.request)
        self.assertIn("Test Project", html)
        self.assertIn("SQL Injection", html)
        self.assertIn("Use prepared statements", html)

    def test_pdf_generation(self):
        # Change format to pdf for this test
        self.request.format = "pdf"
        pdf_bytes = self.pdf_gen.generate_report(self.request)
        self.assertTrue(len(pdf_bytes) > 0)
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))

if __name__ == '__main__':
    unittest.main()
