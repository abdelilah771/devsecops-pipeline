import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.services.html_generator import HtmlGenerator
from app.models import ReportRequest, Vulnerability, ScanMetrics

def render_executive():
    metrics = ScanMetrics(
        total_vulnerabilities=15,
        critical_count=2,
        high_count=5,
        medium_count=3,
        low_count=5,
        security_score=45.5
    )
    
    vulns = [
        Vulnerability(
            id="VULN-1", severity="CRITICAL", category="Injection",
            description="SQL Injection in login", affected_component="AuthService",
            line_number=10, fix_suggestion="Use param queries"
        ),
        Vulnerability(
            id="VULN-2", severity="CRITICAL", category="Broken Access Control",
            description="Admin bypass", affected_component="AdminPanel",
            line_number=42, fix_suggestion="Check roles"
        ),
        Vulnerability(
            id="VULN-3", severity="HIGH", category="XSS",
            description="Stored XSS", affected_component="Comments",
            line_number=100, fix_suggestion="Sanitize input"
        ),
        Vulnerability(
            id="VULN-4", severity="HIGH", category="CSRF",
            description="Missing token", affected_component="Profile",
            line_number=20, fix_suggestion="Add CSRF token"
        )
    ]

    request = ReportRequest(
        run_id="MOCK-RUN-001",
        report_type="executive",
        format="html",
        vulnerabilities=vulns,
        metrics=metrics,
        project_name="Mock Project"
    )

    generator = HtmlGenerator()
    html_output = generator.generate_report(request)

    output_file = "executive_report_mock.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"Generated {output_file}")

if __name__ == "__main__":
    render_executive()
