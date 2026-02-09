from typing import Type, Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from markitdown import MarkItDown
import os


class MarkitdownInput(BaseModel):
    file_path: str = Field(
        ...,
        description="The absolute path to the file (PDF, etc.) to convert to Markdown.",
    )


class MarkitdownTool(BaseTool):
    name: str = "Convert File to Markdown"
    description: str = (
        "A tool that converts various file formats (PDF, PowerPoint, Word, Excel, Images, etc.) "
        "into structured Markdown text using Microsoft's MarkItDown library. "
        "Use this tool to extract text content from documents for analysis."
    )
    args_schema: Type[BaseModel] = MarkitdownInput

    def _run(self, file_path: str) -> str:
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at path: {file_path}"

            md = MarkItDown()
            result = md.convert(file_path)

            if result is None:
                return "Error: specific file conversion failed, result is None."

            return result.text_content

        except Exception as e:
            return f"Error converting file: {str(e)}"
