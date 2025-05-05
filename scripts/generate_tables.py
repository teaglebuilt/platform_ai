from lancedb import connect
import uuid
from random import choice, random
from datetime import datetime, timezone

SAMPLE_TEXTS = [
    "Hexagonal architecture separates domain from infrastructure.",
    "LangChain supports retrieval-augmented generation.",
    "CrewAI orchestrates multi-agent task execution.",
    "DuckDB is great for analytics with SQL.",
    "Rill makes dashboards from DuckDB in seconds."
]

def create_sample_vector(dim: int = 1536):
    return [random() for _ in range(dim)]


def main():
    db = connect("./data/generated/lancedb")
    table_name = "memory"

    if table_name not in db.table_names():
        db.create_table(table_name, data=[
            {"id": str(uuid.uuid4()), "text": "", "vector": [0.0] * 1536, "timestamp": datetime.now(tz=timezone.utc)}
        ])

    table = db.open_table(table_name)
    table.add([
        {
            "id": str(uuid.uuid4()),
            "text": choice(SAMPLE_TEXTS),
            "vector": create_sample_vector(),
            "timestamp": datetime.now(tz=timezone.utc)
        }
        for _ in range(10)
    ])

    print("✅ Sample memory records inserted into LanceDB.")


if __name__ == "__main__":
    main()