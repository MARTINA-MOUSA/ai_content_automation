from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor
import os

def generate_pdf_report(analysis: dict, metadata: dict, output_path: str):
    """Generates a clean PDF report with analysis and metadata."""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=HexColor("#1A73E8")
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=HexColor("#5F6368")
    )

    story = []

    # Title
    title = analysis.get("title", "Content Analysis Report")
    story.append(Paragraph(title, header_style))
    story.append(Spacer(1, 12))

    # Metadata Section
    story.append(Paragraph("<b>METADATA</b>", styles['Heading3']))
    story.append(Paragraph(f"<b>Author:</b> {metadata.get('author', 'Unknown')}", styles['Normal']))
    story.append(Paragraph(f"<b>Date:</b> {metadata.get('date', 'Unknown')}", styles['Normal']))
    story.append(Paragraph(f"<b>Source URL:</b> <link href='{metadata.get('source', '')}'>{metadata.get('source', 'Link')}</link>", styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary Section
    story.append(Paragraph("<b>SUMMARY</b>", styles['Heading3']))
    summary = analysis.get("summary", "No summary available.")
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 12))

    # Key Topics
    topics = analysis.get("key_topics", [])
    if topics:
        story.append(Paragraph("<b>KEY TOPICS</b>", styles['Heading3']))
        topics_text = ", ".join(topics)
        story.append(Paragraph(topics_text, styles['Normal']))
        story.append(Spacer(1, 12))

    # Sentiment
    sentiment = analysis.get("sentiment", "neutral").capitalize()
    story.append(Paragraph(f"<b>SENTIMENT:</b> {sentiment}", styles['Normal']))

    doc.build(story)
    return output_path
