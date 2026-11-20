import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted
)


# =====================================
# 1. FILE PATHS
# =====================================

input_file = "reports/AI_Business_Insights.txt"
output_file = "reports/AI_Business_Intelligence_Report.pdf"


# =====================================
# 2. CHECK INPUT FILE
# =====================================

if not os.path.exists(input_file):
    raise FileNotFoundError(
        "AI insights TXT file not found. Run ai_insights.py first."
    )


# =====================================
# 3. READ AI REPORT
# =====================================

with open(input_file, "r", encoding="utf-8") as file:
    report_text = file.read()


# =====================================
# 4. CREATE PDF DOCUMENT
# =====================================

os.makedirs("reports", exist_ok=True)

pdf = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=55,
    leftMargin=55,
    topMargin=55,
    bottomMargin=55
)


# =====================================
# 5. DEFINE STYLES
# =====================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=21,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10,
    alignment=TA_CENTER,
    textColor=colors.grey,
    spaceAfter=25
)

body_style = ParagraphStyle(
    "ReportBody",
    parent=styles["BodyText"],
    fontSize=10,
    leading=16,
    spaceAfter=10
)


# =====================================
# 6. BUILD PDF CONTENT
# =====================================

story = []

story.append(
    Paragraph(
        "AMAZON PRIME",
        title_style
    )
)

story.append(
    Paragraph(
        "AI-Powered Content Intelligence Report",
        subtitle_style
    )
)

story.append(
    Paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        subtitle_style
    )
)

story.append(Spacer(1, 15))


# Add AI-generated report content

for line in report_text.splitlines():

    line = line.strip()

    if not line:
        story.append(Spacer(1, 8))
        continue

    safe_line = (
        line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )

    if line.startswith("#"):
        story.append(
            Paragraph(
                f"<b>{safe_line.lstrip('# ').strip()}</b>",
                styles["Heading2"]
            )
        )

    elif line[:1].isdigit() and "." in line[:4]:
        story.append(
            Paragraph(
                f"<b>{safe_line}</b>",
                body_style
            )
        )

    else:
        story.append(
            Paragraph(safe_line, body_style)
        )


# =====================================
# 7. GENERATE PDF
# =====================================

pdf.build(story)

print("\n====================================")
print("PDF REPORT GENERATED SUCCESSFULLY!")
print("File:", output_file)
print("====================================")
