"""
title: Repository Training
version: 0.0.1
requirements: llama-index, llama-index-llms-ollama, llama-index-embeddings-ollama, llama-index-readers-github
"""

from typing import List, Union, Generator, Iterator
import os
import asyncio

DEBUG_ENABLED: bool = os.environ["DEBUG"]
OLLAMA_SERVICE: bool = os.environ["OLLAMA_HOST"]


class Pipeline:
    def __init__(self) -> None:
        self.documents = None
        self.index = None

    async def on_startup(self):
        from llama_index.embeddings.ollama import OllamaEmbedding
        from llama_index.llms.ollama import Ollama
        from llama_index.core import VectorStoreIndex, Settings
        from llama_index.readers.github import GithubRepositoryReader, GithubClient

        Settings.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url=OLLAMA_SERVICE,
        )
        Settings.llm = Ollama(model="llama3")

        global index, documents

        github_token = os.environ.get("GITHUB_TOKEN")
        owner = "teaglebuilt"
        repo = "homelab"
        branch = "main"

        github_client = GithubClient(github_token=github_token, verbose=True)

        reader = GithubRepositoryReader(
            github_client=github_client,
            owner=owner,
            repo=repo,
            use_parser=False,
            verbose=DEBUG_ENABLED,
            filter_file_extensions=(
                [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".svg",
                    ".ico",
                    "json",
                    ".ipynb",
                    ".gitkeep"
                ],
                GithubRepositoryReader.FilterType.EXCLUDE,
            ),
        )

        loop = asyncio.new_event_loop()

        reader._loop = loop

        try:
            self.documents = await asyncio.to_thread(reader.load_data, branch=branch)
            self.index = VectorStoreIndex.from_documents(self.documents)
        finally:
            loop.close()

        print(self.documents)
        print(self.index)

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.

        print(messages)
        print(user_message)

        query_engine = self.index.as_query_engine(streaming=True)
        response = query_engine.query(user_message)

        return response.response_gen
