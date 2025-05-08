from pydantic import BaseModel


class CodeChunk(BaseModel):
    filename: str
    text: str

    # text: str = func.SourceField()
    # # 1024 is the default dimension for `voyage-code-3`: https://docs.voyageai.com/docs/embeddings#model-choices
    # vector: Vector(1024) = func.VectorField()