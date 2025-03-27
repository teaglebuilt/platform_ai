from enum import Enum
from langchain.document_loaders import GitLoader, DirectoryLoader
from langchain_community import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import LanceDB
import lancedb

class Loaders(Enum):
    GIT = "GitLoader"
    LOCALDIR = "DirectoryLoader"


def get_loader(loader: Loaders) -> GitLoader | DirectoryLoader:
    loader = getattr(document_loaders, loader)
    return loader
