# Paper Reader Implementation Plan

Based on `AGENTS.md`, this plan outlines the implementation of the Paper Reader Agent system using CrewAI and Markitdown.

## Phase 1: Project Initialization & Environment Setup
- [ ] **Initialize Project Structure**:
    - Create directories: `src/agents`, `src/tools`, `src/tasks`, `output`, `tests`.
    - Set up `pyproject.toml` with `uv`.
- [ ] **Dependency Management**:
    - Add runtime dependencies: `crewai`, `markitdown`, `chromadb`, `langchain-openai`, `python-dotenv`.
    - Add dev dependencies: `pytest`, `ruff`, `mypy`.
- [ ] **Environment Configuration**:
    - Create `.env.example` template (include `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `SERPER_API_KEY`).
    - Set up `.gitignore`.

## Phase 2: Core Tool Implementation
- [ ] **Markitdown Wrapper**:
    - Create `src/tools/markitdown_tool.py`.
    - Implement `MarkitdownTool` class inheriting from `BaseTool` (CrewAI/LangChain compatible).
    - Functionality: Accept PDF file path, return structured Markdown content (including image descriptions if supported).
    - Unit tests: Verify PDF to Markdown conversion with mock/sample file.
- [ ] **Vector Database Integration**:
    - Implement `ChromaDB` wrapper or usage in `Scanning Specialist` to index paper sections for efficient retrieval.

## Phase 3: Agent Configuration
- [ ] **Agent Definitions** (`src/agents/paper_agents.py`):
    - **Skimmer Agent**:
        - Role: "Research Paper Skimmer"
        - Goal: Extract core contributions and outline.
        - Backstory: Experienced researcher adept at quickly identifying key insights.
    - **Scanning Specialist**:
        - Role: "Technical Deep Dive Analyst"
        - Goal: Extract detailed methodologies and experimental setups.
        - Backstory: Detail-oriented analyst focusing on reproducibility.
    - **Critical Reviewer**:
        - Role: "Critical Paper Reviewer"
        - Goal: Validate claims against evidence and identify limitations.
        - Backstory: Skeptical reviewer ensuring scientific rigor.

## Phase 4: Task Definitions
- [ ] **Task Definitions** (`src/tasks/paper_tasks.py`):
    - **Preprocessing Task**:
        - Description: Convert PDF to Markdown using `MarkitdownTool`.
        - Output: Raw Markdown content (saved to `temp_paper.md` or passed in context).
    - **Skimming Task**:
        - Description: Analyze the Markdown to produce a "Research Summary Card".
        - Agent: Skimmer.
    - **Deep Dive Task**:
        - Description: Analyze specific sections (Methods, Results) based on the summary.
        - Agent: Scanning Specialist.
    - **Validation Task**:
        - Description: Critically review findings and check logical consistency.
        - Agent: Critical Reviewer.

## Phase 5: Workflow Orchestration
- [ ] **Main Execution Script** (`src/main.py`):
    - Load environment variables.
    - Configure LLM (Claude 3.5 Sonnet, GPT-4o, or Deepseek-v3.2) for agents.
    - Instantiate Agents and Tasks.
    - Create `Crew` with sequential process.
    - Define input mechanism (CLI argument for PDF path).
    - Execute crew and handle output.

## Phase 6: Testing & Validation
- [ ] **Unit Testing**:
    - Test `MarkitdownTool` independently.
    - Test individual agent prompt templates (if custom).
- [ ] **Integration Testing**:
    - Run the full pipeline with a sample PDF.
    - Verify output structure and content quality.
