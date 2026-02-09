import os
import argparse
from dotenv import load_dotenv
from crewai import Crew, Process, LLM
from src.agents.paper_agents import PaperAgents
from src.tasks.paper_tasks import PaperTasks
from src.tools.vector_db_tool import PaperIndexer
from src.tools.markitdown_tool import MarkitdownTool


def setup_llm():
    if os.getenv("DEEPSEEK_API_KEY"):
        return LLM(
            model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
    elif os.getenv("ANTHROPIC_API_KEY"):
        return LLM(
            model=os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-5-sonnet-20241022"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        raise ValueError(
            "No API key found. Please set DEEPSEEK_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY in .env"
        )


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Paper Reader Agent System")
    parser.add_argument("pdf_path", help="Path to the PDF paper to analyze")
    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf_path)
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    try:
        llm = setup_llm()
        print(f"Using LLM: {llm.model}")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("Preprocessing: Converting PDF to Markdown...")
    md_tool = MarkitdownTool()
    markdown_content = md_tool._run(pdf_path)

    if markdown_content.startswith("Error"):
        print(markdown_content)
        return

    print("Preprocessing: Indexing content...")
    indexer = PaperIndexer()
    indexer.index_content(markdown_content, source=os.path.basename(pdf_path))

    with open("temp_paper.md", "w") as f:
        f.write(markdown_content)

    agents = PaperAgents(llm)
    tasks = PaperTasks()

    skimmer = agents.skimmer_agent()
    scanner = agents.scanning_specialist_agent()
    reviewer = agents.critical_reviewer_agent()

    task_skim = tasks.skimming_task(skimmer, [])
    task_skim.description += (
        f"\n\nHere is the full paper content:\n\n{markdown_content}"
    )

    task_deep = tasks.deep_dive_task(scanner, [task_skim])
    task_valid = tasks.validation_task(reviewer, [task_deep])

    crew = Crew(
        agents=[skimmer, scanner, reviewer],
        tasks=[task_skim, task_deep, task_valid],
        process=Process.sequential,
        verbose=True,
    )

    print("Starting analysis...")
    result = crew.kickoff()

    print("\n\n########################")
    print("## Final Analysis Result ##")
    print("########################\n")
    print(result)

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_analysis.md")
    with open(output_path, "w") as f:
        f.write(str(result))
    print(f"\nAnalysis saved to {output_path}")


if __name__ == "__main__":
    main()
