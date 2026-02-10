from crewai import Agent
from src.tools.vector_db_tool import VectorDBTool


class PaperAgents:
    def __init__(self, llm):
        self.llm = llm

    def skimmer_agent(self):
        return Agent(
            role="Research Paper Skimmer",
            goal="Extract core contributions, key problems solved, and the overall logical structure of the paper.",
            backstory=(
                "You are an expert researcher with a talent for quickly identifying the essence of complex scientific papers. "
                "You don't get lost in details but focus on the 'big picture': What is this about? Why does it matter? "
                "What are the main claims? You are the first pass filter for the research team."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def scanning_specialist_agent(self):
        return Agent(
            role="Technical Deep Dive Analyst",
            goal="Extract detailed methodologies, experimental setups, and analyze charts/diagrams description.",
            backstory=(
                "You are a meticulous technical analyst. Your job is to verify reproducibility and understand the 'how'. "
                "You dive deep into the Methods and Results sections. You use semantic search to find specific details "
                "about parameters, algorithms, and data processing steps. You ignore the fluff and focus on the mechanics."
            ),
            tools=[VectorDBTool()],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def critical_reviewer_agent(self):
        return Agent(
            role="Critical Paper Reviewer",
            goal="Critically evaluate the paper's claims against its evidence and identify limitations.",
            backstory=(
                "You are a skeptical senior reviewer. You don't take claims at face value. "
                "You check if the results actually support the conclusion. You look for logical gaps, "
                "missing baselines, or overclaimed results. You provide a balanced but critical assessment "
                "of the paper's true impact."
            ),
            tools=[VectorDBTool()],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
        )

    def summary_agent(self):
        return Agent(
            role="Lead Research Summarizer",
            goal="Synthesize the outputs from the Skimmer, Scanning Specialist, and Critical Reviewer to create a comprehensive final report.",
            backstory=(
                "You are the lead editor of a prestigious journal. Your job is to take the raw analysis from your team "
                "(skimming, deep dive, and critique) and compile it into a polished, easy-to-read executive summary "
                "for the decision makers. You ensure the tone is professional, the structure is clear, and all key insights are captured."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )
