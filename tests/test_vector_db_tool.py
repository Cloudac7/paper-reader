import pytest
from unittest.mock import patch, MagicMock
from src.tools.vector_db_tool import VectorDBTool, PaperIndexer


@patch("src.tools.vector_db_tool.chromadb.PersistentClient")
def test_indexer_index_content(mock_client_cls):
    mock_client = mock_client_cls.return_value
    mock_collection = mock_client.get_or_create_collection.return_value
    mock_collection.count.return_value = 0

    indexer = PaperIndexer()
    content = "Chunk 1\n\nChunk 2"
    result = indexer.index_content(content)

    assert "Indexed 2 chunks" in result
    mock_collection.add.assert_called_once()

    call_args = mock_collection.add.call_args
    assert len(call_args.kwargs["documents"]) == 2
    assert call_args.kwargs["documents"][0] == "Chunk 1"
    assert call_args.kwargs["documents"][1] == "Chunk 2"


@patch("src.tools.vector_db_tool.chromadb.PersistentClient")
def test_vector_db_tool_run_found(mock_client_cls):
    mock_client = mock_client_cls.return_value
    mock_collection = mock_client.get_or_create_collection.return_value

    mock_collection.query.return_value = {
        "documents": [["Doc 1", "Doc 2"]],
        "metadatas": [
            [{"source": "paper", "chunk_id": "1"}, {"source": "paper", "chunk_id": "2"}]
        ],
        "ids": [["1", "2"]],
    }

    tool = VectorDBTool()
    result = tool._run("query")

    assert "--- Result 1 (Source: paper, Chunk: 1) ---" in result
    assert "Doc 1" in result
    assert "--- Result 2 (Source: paper, Chunk: 2) ---" in result
    assert "Doc 2" in result


@patch("src.tools.vector_db_tool.chromadb.PersistentClient")
def test_vector_db_tool_run_not_found(mock_client_cls):
    mock_client = mock_client_cls.return_value
    mock_collection = mock_client.get_or_create_collection.return_value

    mock_collection.query.return_value = {
        "documents": [[]],
        "metadatas": [[]],
        "ids": [[]],
    }

    tool = VectorDBTool()
    result = tool._run("query")

    assert "No relevant content found matching the query." == result
