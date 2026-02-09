import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from src.main import main


@patch("src.main.Crew")
@patch("src.agents.paper_agents.Agent")
@patch("src.tasks.paper_tasks.Task")
@patch("src.main.MarkitdownTool")
@patch("src.main.PaperIndexer")
@patch("src.main.setup_llm")
@patch("os.path.exists")
@patch("src.main.argparse.ArgumentParser")
@patch("builtins.open", new_callable=MagicMock)
def test_main_flow(
    mock_open,
    mock_argparse_cls,
    mock_exists,
    mock_setup_llm,
    mock_indexer_cls,
    mock_md_tool_cls,
    mock_task_cls,
    mock_agent_cls,
    mock_crew_cls,
):
    mock_exists.return_value = True

    mock_llm = MagicMock()
    mock_llm.model = "test-model"
    mock_setup_llm.return_value = mock_llm

    mock_md_instance = mock_md_tool_cls.return_value
    mock_md_instance._run.return_value = "# Test Paper\n\nContent"

    mock_indexer_instance = mock_indexer_cls.return_value

    mock_crew_instance = mock_crew_cls.return_value
    mock_crew_instance.kickoff.return_value = "Final Analysis Result"

    mock_task_instance = mock_task_cls.return_value
    mock_task_instance.description = "Base description"

    mock_parser = mock_argparse_cls.return_value
    mock_args = MagicMock()
    mock_args.pdf_path = "test_paper.pdf"
    mock_parser.parse_args.return_value = mock_args

    main()

    mock_setup_llm.assert_called_once()

    mock_md_instance._run.assert_called()
    args, _ = mock_md_instance._run.call_args
    assert args[0].endswith("test_paper.pdf")

    mock_indexer_instance.index_content.assert_called()

    assert mock_agent_cls.call_count == 3
    assert mock_task_cls.call_count == 3

    mock_crew_instance.kickoff.assert_called_once()

    assert mock_open.call_count >= 2
