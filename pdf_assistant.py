import typer
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage #creates storage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import os
from dotenv import load_dotenv
os.environ["GROQ_API_KEY"] = "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"
load_dotenv()
from financial_agent import generate_report
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def save_pdf(text, filename):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line.replace("\t", "&nbsp;"*4), styles["BodyText"]))
    doc.build(story)

report = generate_report()

#save_pdf(report, "financial_report.pdf")

