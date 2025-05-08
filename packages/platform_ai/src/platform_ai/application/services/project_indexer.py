import os
from pathlib import Path
from lancedb.pydantic import Vector, pydantic_to_schema
from lancedb.embeddings import get_registry
import lancedb

# from platform_ai.domain.models.code import CodeChunk

# db = lancedb.connect("/tmp/db")
# func = get_registry().get("openai").create(
#     name="voyage-code-3",
#     base_url="https://api.voyageai.com/v1/",
#     api_key=os.environ["VOYAGE_API_KEY"],
# )


# class RepoCodeChunks(CodeChunk):
#     vector = Vector(1024)


def initialize():
    breakpoint()
    continue_db = lancedb.connect(str(Path(os.path.expanduser("~")) / ".continue" / "index" / "lancedb"))
    # schema = pydantic_to_schema(RepoCodeChunks)
    # table = db.create_table("code_chunks", schema=schema)
    # table = db.create_table("projects", schema=schema)
    # table.add([
    #     {"text": "print('hello world!')", "filename": "hello.py"},
    #     {"text": "print('goodbye world!')", "filename": "goodbye.py"}
    # ])
