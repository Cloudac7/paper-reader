from crewai import Task
from textwrap import dedent


class PaperTasks:
    def preprocessing_task(self, agent, file_path):
        return Task(
            description=dedent(f"""
                Read the paper at '{file_path}' using the Markitdown tool.
                This is a pre-processing step to extract the text content.
                Ensure the extracted content is structured and comprehensive.
            """),
            expected_output="The full markdown text content of the paper.",
            agent=agent,
        )

    def skimming_task(self, agent, context):
        return Task(
            description=dedent("""
                Analyze the paper content provided in the context.
                1. Read the Title, Abstract, Introduction, and Conclusion.
                2. Identify the core problem the paper solves.
                3. Summarize the main contribution and the proposed method's high-level logic.
                4. Create a 'Research Summary Card' with these details.
            """),
            expected_output="A Markdown formatted Research Summary Card with sections: Title, Problem, Contribution, Method Overview, Structure.",
            agent=agent,
            context=context,
        )

    def deep_dive_task(self, agent, context):
        return Task(
            description=dedent("""
                Based on the summary provided, perform a deep dive into the technical details.
                1. Use the vector search tool (if available) to find details about the Methodology and Experiments.
                2. Extract the specific algorithms, equations, or system architecture described.
                3. Analyze the experimental setup and results.
                4. Specifically look for 'how' it works, not just 'what' it does.
            """),
            expected_output="A technical report detailing the Methodology (step-by-step), Experimental Setup, and Key Results (with metrics).",
            agent=agent,
            context=context,
        )

    def validation_task(self, agent, context):
        return Task(
            description=dedent("""
                Review the technical report and the original paper's claims.
                1. Verify if the experimental results usually support the claims made in the summary.
                2. Identify any limitations, assumptions, or potential weak points mentioned or implied.
                3. Provide a critical assessment of the paper's reliability and impact.
            """),
            expected_output="A Critical Review Report listing: Strengths, Weaknesses, unsupported claims, and overall assessment.",
            agent=agent,
            context=context,
        )
