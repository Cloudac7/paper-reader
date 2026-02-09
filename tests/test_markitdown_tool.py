import pytest
import os
from unittest.mock import patch, MagicMock
from src.tools.markitdown_tool import MarkitdownTool


@pytest.fixture
def tool():
    return MarkitdownTool()


def test_tool_initialization(tool):
    assert tool.name == "Convert File to Markdown"
    assert "A tool that converts various file formats" in tool.description


@patch("src.tools.markitdown_tool.MarkItDown")
@patch("os.path.exists")
def test_run_success(mock_exists, mock_markitdown, tool):
    mock_exists.return_value = True

    mock_instance = mock_markitdown.return_value
    mock_result = MagicMock()
    mock_result.text_content = "# Title\n\nContent of the PDF."
    mock_instance.convert.return_value = mock_result

    file_path = "/path/to/test.pdf"
    result = tool._run(file_path)

    assert result == "# Title\n\nContent of the PDF."
    mock_markitdown.assert_called_once()
    mock_instance.convert.assert_called_once_with(file_path)


@patch("os.path.exists")
def test_run_file_not_found(mock_exists, tool):
    mock_exists.return_value = False

    file_path = "/path/to/missing.pdf"
    result = tool._run(file_path)

    assert f"Error: File not found at path: {file_path}" == result


@patch("src.tools.markitdown_tool.MarkItDown")
@patch("os.path.exists")
def test_run_exception(mock_exists, mock_markitdown, tool):
    mock_exists.return_value = True

    mock_instance = mock_markitdown.return_value
    mock_instance.convert.side_effect = Exception("Conversion failed")

    file_path = "/path/to/broken.pdf"
    result = tool._run(file_path)

    assert "Error converting file: Conversion failed" in result


@patch("src.tools.markitdown_tool.MarkItDown")
@patch("os.path.exists")
def test_run_none_result(mock_exists, mock_markitdown, tool):
    mock_exists.return_value = True

    mock_instance = mock_markitdown.return_value
    mock_instance.convert.return_value = None

    file_path = "/path/to/empty.pdf"
    result = tool._run(file_path)

    assert "Error: specific file conversion failed, result is None." == result
