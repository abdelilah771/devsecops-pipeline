from jinja2 import Environment, FileSystemLoader
import os
from app.models import ReportRequest
from app.services.chart_service import ChartService

class HtmlGenerator:
    def __init__(self, template_dir: str = "app/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_report(self, request: ReportRequest) -> str:
        """
        Generates HTML report based on the report type and request data.
        """
        template_name = f"{request.report_type}.html"
        template = self.env.get_template(template_name)
        
        # Generate charts
        pie_chart = ChartService.generate_severity_pie_chart(request.metrics)
        bar_chart = ChartService.generate_category_bar_chart(request.vulnerabilities)

        # Render template
        html_content = template.render(
            request=request,
            metrics=request.metrics,
            vulnerabilities=request.vulnerabilities,
            pie_chart=pie_chart,
            bar_chart=bar_chart
        )
        return html_content
