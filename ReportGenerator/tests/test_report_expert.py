
import unittest
from unittest.mock import MagicMock, patch
from app.models import ReportRequest, ScanMetrics, Vulnerability, FixProposal
from app.services.html_generator import HtmlGenerator
import os

class TestExpertReport(unittest.TestCase):
    def setUp(self):
        self.html_gen = HtmlGenerator()
        
    def test_generate_technical_report_content(self):
        # Mock Request with one vulnerability having a fix
        vuln = Vulnerability(
            id="1",
            severity="HIGH",
            category="SQL Injection",
            description="SQL Injection in login form",
            affected_component="auth.py",
            line_number=42,
            fix_suggestion="Use parameterized queries",
            cve_id="CVE-2021-1234"
        )
        metrics = ScanMetrics(
            total_vulnerabilities=1,
            critical_count=0,
            high_count=1,
            medium_count=0,
            low_count=0,
            security_score=8.5
        )
        request = ReportRequest(
            run_id="test-run-001",
            report_type="technical",
            format="html",
            vulnerabilities=[vuln],
            metrics=metrics,
            project_name="Test Project",
            triggered_by="Unit Test"
        )
        
        # Generate HTML
        html_content = self.html_gen.generate_report(request)
        
        # Verify content
        self.assertIn("Security Assessment Report", html_content)
        self.assertIn("Prepared by DevSecOps Pipeline", html_content)
        self.assertIn("Executive Summary", html_content)
        self.assertIn("SQL Injection", html_content)
        self.assertIn("Recommended Fix:", html_content)
        self.assertIn("Use parameterized queries", html_content)
        self.assertIn("Detailed Findings & Remediation", html_content)

if __name__ == '__main__':
    unittest.main()
