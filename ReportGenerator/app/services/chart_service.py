import matplotlib.pyplot as plt
import io
import base64
from app.models import ScanMetrics, Vulnerability
from typing import List

class ChartService:
    @staticmethod
    def generate_severity_pie_chart(metrics: ScanMetrics) -> str:
        """Generates a pie chart for vulnerability severity distribution and returns base64 string."""
        labels = ['Critical', 'High', 'Medium', 'Low']
        sizes = [metrics.critical_count, metrics.high_count, metrics.medium_count, metrics.low_count]
        colors = ['#ff4d4d', '#ffad33', '#ffff66', '#66ff66']
        explode = (0.1, 0, 0, 0)  # explode 1st slice

        # Filter out zero values to avoid messy charts
        filtered_data = [(l, s, c, e) for l, s, c, e in zip(labels, sizes, colors, explode) if s > 0]
        if not filtered_data:
             return "" # No data to chart

        labels, sizes, colors, explode = zip(*filtered_data)

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Vulnerability Severity Distribution')

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        return img_str

    @staticmethod
    def generate_category_bar_chart(vulnerabilities: List[Vulnerability]) -> str:
        """Generates a horizontal bar chart for OWASP categories."""
        categories = {}
        for v in vulnerabilities:
            categories[v.category] = categories.get(v.category, 0) + 1

        if not categories:
            return ""

        sorted_categories = sorted(categories.items(), key=lambda item: item[1], reverse=True)
        cats = [x[0] for x in sorted_categories]
        counts = [x[1] for x in sorted_categories]

        plt.figure(figsize=(10, 6))
        plt.barh(cats, counts, color='skyblue')
        plt.xlabel('Count')
        plt.title('Vulnerabilities by Category')
        plt.gca().invert_yaxis() # Highest count at top

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        return img_str
