import chromadb
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import uuid
from typing import Type

DB_PATH = os.path.join(os.getcwd(), "chroma_db")


class VectorSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The semantic query string to search for related content in the paper. IMPORTANT: Always use ENGLISH for the query to maximize retrieval performance.",
    )
    n_results: int = Field(
        default=3, description="Number of results to return (default: 3)."
    )


class VectorDBTool(BaseTool):
    name: str = "Search Paper Content"
    description: str = (
        "Search for relevant sections in the paper using semantic search. "
        "Use this tool to find specific details, methods, or results mentioned in the text."
    )
    args_schema: Type[BaseModel] = VectorSearchInput

    collection_name: str = "paper_content"
    persist_directory: str = DB_PATH

    def _run(self, query: str, n_results: int = 3) -> str:
        try:
            client = chromadb.PersistentClient(path=self.persist_directory)
            collection = client.get_or_create_collection(name=self.collection_name)

            results = collection.query(query_texts=[query], n_results=n_results)

            output = []
            documents = results.get("documents")
            metadatas = results.get("metadatas")

            if documents and documents[0]:
                for i, doc in enumerate(documents[0]):
                    meta = {}
                    if metadatas and metadatas[0]:
                        meta = metadatas[0][i]  # type: ignore

                    source = str(meta.get("source", "Unknown"))
                    chunk_id = str(meta.get("chunk_id", "Unknown"))
                    output.append(
                        f"--- Result {i + 1} (Source: {source}, Chunk: {chunk_id}) ---\n{doc}\n"
                    )

            if not output:
                return "No relevant content found matching the query."

            return "\n".join(output)

        except Exception as e:
            return f"Error searching vector database: {str(e)}"


class PaperIndexer:
    def __init__(
        self, persist_directory: str = DB_PATH, collection_name: str = "paper_content"
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def index_content(self, content: str, source: str = "paper"):
        try:
            if self.collection.count() > 0:
                self.client.delete_collection(self.collection_name)
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name
                )
        except Exception:
            pass

        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

        if not chunks:
            return "No content to index."

        ids = [f"{source}_{uuid.uuid4()}" for _ in range(len(chunks))]
        metadatas = [
            {"source": source, "chunk_index": i, "chunk_id": ids[i]}
            for i in range(len(chunks))
        ]

        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas,  # type: ignore
        )
        return f"Indexed {len(chunks)} chunks from {source}."
