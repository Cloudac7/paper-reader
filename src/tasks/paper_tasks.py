from crewai import Task
from textwrap import dedent


class PaperTasks:
    def preprocessing_task(self, agent, file_path):
        return Task(
            description=dedent(f"""
                Read the paper at '{file_path}' using the MinerU tool.
                This is a pre-processing step to extract the text content.
                Ensure the extracted content is structured and comprehensive.
            """),
            expected_output="The full markdown text content of the paper.",
            agent=agent,
        )

    def skimming_task(self, agent, context, output_file=None, language="Chinese"):
        return Task(
            description=dedent(f"""
                Analyze the paper content provided in the context.
                1. Read the Title, Abstract, Introduction, and Conclusion.
                2. Identify the core problem the paper solves.
                3. Summarize the main contribution and the proposed method's high-level logic.
                4. Create a 'Research Summary Card' with these details.
                
                IMPORTANT: The final output must be written in {language}.
            """),
            expected_output=f"A Markdown formatted Research Summary Card with sections: Title, Problem, Contribution, Method Overview, Structure. Written in {language}.",
            agent=agent,
            context=context,
            output_file=output_file,
        )

    def deep_dive_task(self, agent, context, output_file=None, language="Chinese"):
        return Task(
            description=dedent(f"""
                Based on the summary provided, perform a deep dive into the technical details.
                1. Use the vector search tool (if available) to find details about the Methodology and Experiments.
                2. Extract the specific algorithms, equations, or system architecture described.
                3. Analyze the experimental setup and results.
                4. Specifically look for 'how' it works, not just 'what' it does.
                
                IMPORTANT: The final output must be written in {language}.
            """),
            expected_output=f"A technical report detailing the Methodology (step-by-step), Experimental Setup, and Key Results (with metrics). Written in {language}.",
            agent=agent,
            context=context,
            output_file=output_file,
        )

    def validation_task(self, agent, context, output_file=None, language="Chinese"):
        return Task(
            description=dedent(f"""
                Review the technical report and the original paper's claims.
                1. Verify if the experimental results usually support the claims made in the summary.
                2. Identify any limitations, assumptions, or potential weak points mentioned or implied.
                3. Provide a critical assessment of the paper's reliability and impact.
                
                IMPORTANT: The final output must be written in {language}.
            """),
            expected_output=f"A Critical Review Report listing: Strengths, Weaknesses, unsupported claims, and overall assessment. Written in {language}.",
            agent=agent,
            context=context,
            output_file=output_file,
        )

    def summary_task(self, agent, context, output_file=None, language="Chinese"):
        return Task(
            description=dedent(f"""
                Synthesize the outputs from the previous agents (Research Summary Card, Technical Deep Dive, Critical Review)
                into a single, cohesive final report.
                The report MUST contain:
                1. Title
                2. Executive Summary (Abstract/Gist)
                3. Methodology Overview (synthesized from deep dive)
                4. Key Results & Metrics
                5. Conclusion
                6. Evaluation (from critical review)
                Ensure the formatting is consistent Markdown.
                
                IMPORTANT: The final output must be written in {language}.
            """),
            expected_output=f"A final, comprehensive Markdown report including Title, Executive Summary, Methodology, Results, Conclusion, and Evaluation. Written in {language}.",
            agent=agent,
            context=context,
            output_file=output_file,
        )
