# Paper Reader Agent (论文智能解析助手)

**[English](#english) | [中文](docs/README_zh-cn.md)**

**Paper Reader** is an intelligent agentic system designed to deeply analyze scientific papers (PDFs). Built on **CrewAI** and **OpenDataLab MinerU**, it simulates the reading workflow of expert researchers—skimming, deep diving, validating, and summarizing—to extract structured, high-quality insights.

## ✨ Key Features

*   **High-Fidelity Parsing**: Uses [MinerU](https://github.com/opendatalab/MinerU) (Magic-PDF) to convert PDFs into structured Markdown, accurately preserving formulas, tables, and layouts.
*   **Multi-Agent Collaboration**:
    *   **Skimmer**: Extracts core contributions and logical structure.
    *   **Scanning Specialist**: Performs technical deep dives using semantic vector search (always querying in English for best results).
    *   **Critical Reviewer**: Validates claims against evidence and identifies limitations.
    *   **Summarizer**: Synthesizes all findings into a cohesive final report.
*   **Multilingual Output**: Generates reports in your preferred language (default: Chinese), while maintaining rigorous English-based retrieval for accuracy.
*   **Traceable Process**: Saves intermediate outputs from every agent for transparency.

## 🛠️ Installation

1.  **Prerequisites**:
    *   Python >= 3.13
    *   [uv](https://github.com/astral-sh/uv) (recommended for dependency management)
    *   **Mineru Environment**: Ensure Mineru is installed. By default, the system looks for the binary at `mineru-env/bin/mineru`. You can customize this via the `MINERU_BIN_PATH` environment variable.

2.  **Clone and Sync**:
    ```bash
    git clone https://github.com/your-username/paper-reader.git
    cd paper-reader
    uv sync
    ```

3.  **Configuration**:
    Create a `.env` file in the root directory:
    ```ini
    # Choose your LLM Provider
    DEEPSEEK_API_KEY=sk-
    # OR
    ANTHROPIC_API_KEY=sk-
    # OR
    OPENAI_API_KEY=sk-

    # Optional: Custom path to Mineru binary if not in default location
    # MINERU_BIN_PATH=/path/to/mineru
    ```

## 🚀 Usage

Run the main script with the path to your PDF file:

```bash
# Default (Generates report in Chinese)
uv run python src/main.py papers/demo.pdf

# Generate report in English
uv run python src/main.py papers/demo.pdf --language English

# Generate report in Japanese
uv run python src/main.py papers/demo.pdf -l Japanese
```

## 📂 Output Structure

All results are saved in the `output/` directory:
*   `{paper}_1_skimming.md`: Research Summary Card.
*   `{paper}_2_deep_dive.md`: Detailed methodology and experiments.
*   `{paper}_3_validation.md`: Critical review and limitations.
*   `{paper}_4_summary.md`: **Final Executive Report**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
