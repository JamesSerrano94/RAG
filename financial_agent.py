#.\.venv\Scripts\Activate.ps1
#python --version
#needs to be 3.10, phidata needs to be installed
from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from xml.sax.saxutils import escape
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
from dotenv import load_dotenv
os.environ["GROQ_API_KEY"] = "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"
load_dotenv()

def save_pdf(text, filename="financial_report.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for line in text.splitlines():
        if line.strip():
            story.append(Preformatted(escape(line), styles["Code"]))
            story.append(Spacer(1, 6))
    doc.build(story)

## web search agent
web_search_agent = Agent(name = "Web Search Agent", role = "Search the web for the information",
                         model = Groq(id = "llama-3.3-70b-versatile"),
                         tools = [DuckDuckGo()], instructions = ["Alway include sources"],
                         show_tools_calls = True, markdown = True)
## Financial agent
finance_agent = Agent(name = "Finance AI Agent",
                      model = Groq(id = "llama-3.3-70b-versatile"),
                      tools = [YFinanceTools(stock_price = True, analyst_recommendations = True,
                                             stock_fundamentals = True, company_news = True)],
                      instructions = ["Use tables to display the data"], show_tool_calls = True,
                      markdown = True)
multi_ai_agent = Agent(model = Groq(id = "llama-3.3-70b-versatile"),
                       team = [finance_agent],
                       instructions = ["Use table to display the data"],
                       show_tool_calls = True, markdown = True)



response = multi_ai_agent.run(
    "Summarize analyst recommendation for NVDA using tables.")

save_pdf(response.content, "financial_report.pdf")

print("Task has successfully completed!")