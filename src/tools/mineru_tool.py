import os
import subprocess
import tempfile
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MinerUInput(BaseModel):
    file_path: str = Field(
        ...,
        description="The absolute path to the PDF file to convert to Markdown.",
    )


class MinerUTool(BaseTool):
    name: str = "MinerU PDF to Markdown"
    description: str = (
        "A tool that converts PDF files into structured Markdown text using OpenDataLab's Mineru. "
        "It handles text, tables, and images, providing a comprehensive markdown representation. "
        "Use this as the primary tool for reading PDF papers."
    )
    args_schema: Type[BaseModel] = MinerUInput
    mineru_bin_path: str = os.getenv(
        "MINERU_BIN_PATH", "/home/cloudac7/Project/paper-reader/mineru-env/bin/mineru"
    )

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: File not found at path: {file_path}"

        if not os.path.exists(self.mineru_bin_path):
            return f"Error: Mineru binary not found at {self.mineru_bin_path}. Please ensure Mineru is installed in the expected environment."

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                cmd = [
                    self.mineru_bin_path,
                    "-p",
                    file_path,
                    "-o",
                    temp_dir,
                    "-b",
                    "hybrid-auto-engine",
                    "--source",
                    "modelscope",
                ]

                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=False
                )

                if result.returncode != 0:
                    return f"Error running Mineru: {result.stderr}\nStdout: {result.stdout}"

                filename_stem = os.path.splitext(os.path.basename(file_path))[0]

                found_md = None
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".md") and not file.endswith("_readme.md"):
                            found_md = os.path.join(root, file)
                            if file == f"{filename_stem}.md":
                                break
                    if found_md and os.path.basename(found_md) == f"{filename_stem}.md":
                        break

                if not found_md:
                    return f"Error: Markdown file not generated in output. Stdout: {result.stdout}"

                with open(found_md, "r", encoding="utf-8") as f:
                    content = f.read()

                return content

            except Exception as e:
                return f"Error converting file with Mineru: {str(e)}"
