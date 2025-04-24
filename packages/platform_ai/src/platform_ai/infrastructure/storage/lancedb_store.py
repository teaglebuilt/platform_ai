from lancedb import connect
from langchain_openai.embeddings import OpenAIEmbeddings
from typing import List, Dict
import uuid


class LanceDBStore:
    def __init__(self, db_path: str = "./data/lancedb", table_name: str = "memory"):
        self.db = connect(db_path)
        self.embeddings = OpenAIEmbeddings()

        if table_name not in self.db.table_names():
            self.db.create_table(table_name, data=[
                {"id": str(uuid.uuid4()), "text": "", "vector": [0.0] * 1536}
            ])

        self.table = self.db.open_table(table_name)

    def add_documents(self, docs: List[Dict]):
        texts = [doc["text"] for doc in docs]
        vectors = self.embeddings.embed_documents(texts)
        self.table.add([
            {"id": str(uuid.uuid4()), "text": doc["text"], "vector": vector}
            for doc, vector in zip(docs, vectors)
        ])

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        vector = self.embeddings.embed_query(query)
        return self.table.search(vector).limit(top_k).to_list()
