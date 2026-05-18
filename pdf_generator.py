from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
import re


def clean_html(text):

    if not text:
        return ""

    # Unsupported HTML tags remove
    text = re.sub(r'<h1.*?>', '<b>', text)
    text = re.sub(r'</h1>', '</b><br/><br/>', text)

    text = re.sub(r'<h2.*?>', '<b>', text)
    text = re.sub(r'</h2>', '</b><br/><br/>', text)

    text = re.sub(r'<h3.*?>', '<b>', text)
    text = re.sub(r'</h3>', '</b><br/><br/>', text)

    text = re.sub(r'<p.*?>', '', text)
    text = re.sub(r'</p>', '<br/><br/>', text)

    text = re.sub(r'<ul.*?>', '', text)
    text = re.sub(r'</ul>', '<br/>', text)

    text = re.sub(r'<li.*?>', '• ', text)
    text = re.sub(r'</li>', '<br/>', text)

    # FIX FOR ERROR
    text = re.sub(r'<br>', '<br/>', text)

    # Remove unsupported tags
    text = re.sub(r'</?div.*?>', '', text)

    return text


def generate_pdf(filename, questions):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>AI Exam Analyzer Notes</b>",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    for item in questions:

        question = Paragraph(
            f"<b>Q.</b> {item['question']}",
            styles['Heading3']
        )

        # CLEAN HTML BEFORE PDF
        clean_answer = clean_html(item['answer'])

        answer = Paragraph(
            clean_answer,
            styles['BodyText']
        )

        elements.append(question)

        elements.append(
            Spacer(1, 8)
        )

        elements.append(answer)

        elements.append(
            Spacer(1, 20)
        )

    doc.build(elements)
