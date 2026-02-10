import pytest
from unittest.mock import patch, MagicMock
from src.tools.mineru_tool import MinerUTool


@pytest.fixture
def tool():
    return MinerUTool()


def test_tool_initialization(tool):
    assert tool.name == "MinerU PDF to Markdown"
    assert "converts PDF files" in tool.description


@patch("src.tools.mineru_tool.os.path.exists")
@patch("src.tools.mineru_tool.subprocess.run")
@patch("src.tools.mineru_tool.tempfile.TemporaryDirectory")
@patch("src.tools.mineru_tool.os.walk")
@patch("builtins.open", new_callable=MagicMock)
def test_run_success(mock_open, mock_walk, mock_temp_dir, mock_run, mock_exists, tool):
    mock_exists.return_value = True

    mock_temp_dir.return_value.__enter__.return_value = "/tmp/temp_dir"

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    # Mock os.walk to return a .md file
    # os.walk yields (root, dirs, files)
    mock_walk.return_value = [("/tmp/temp_dir", [], ["test.md"])]

    mock_file = MagicMock()
    mock_file.read.return_value = "# Content"
    mock_open.return_value.__enter__.return_value = mock_file

    file_path = "/path/to/test.pdf"
    # We need to mock os.path.basename and os.path.splitext if logic depends on it
    # But for now assume os.path works

    result = tool._run(file_path)

    assert result == "# Content"
    mock_run.assert_called_once()
    assert "/path/to/test.pdf" in mock_run.call_args[0][0]


@patch("src.tools.mineru_tool.os.path.exists")
def test_run_file_not_found(mock_exists, tool):
    mock_exists.return_value = False

    file_path = "/path/to/missing.pdf"
    result = tool._run(file_path)

    assert f"Error: File not found at path: {file_path}" == result


@patch("src.tools.mineru_tool.os.path.exists")
def test_run_binary_not_found(mock_exists, tool):
    # First call checks file_path (True), second checks binary_path (False)
    mock_exists.side_effect = [True, False]

    file_path = "/path/to/test.pdf"
    result = tool._run(file_path)

    assert "Error: Mineru binary not found" in result


@patch("src.tools.mineru_tool.os.path.exists")
@patch("src.tools.mineru_tool.subprocess.run")
@patch("src.tools.mineru_tool.tempfile.TemporaryDirectory")
def test_run_subprocess_error(mock_temp_dir, mock_run, mock_exists, tool):
    mock_exists.return_value = True
    mock_temp_dir.return_value.__enter__.return_value = "/tmp/temp_dir"

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Process failed"
    mock_result.stdout = ""
    mock_run.return_value = mock_result

    file_path = "/path/to/test.pdf"
    result = tool._run(file_path)

    assert "Error running Mineru" in result
    assert "Process failed" in result
