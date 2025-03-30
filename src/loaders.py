from typing import Union
from enum import Enum
from langchain.document_loaders import GitLoader, DirectoryLoader, RecursiveUrlLoader
from langchain_community import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import LanceDB
import lancedb

LoaderType = Union[GitLoader, DirectoryLoader, RecursiveUrlLoader]

class Loaders(Enum):
    URL = "RecursiveUrlLoader"
    GIT = "GitLoader"
    LOCALDIR = "DirectoryLoader"


def get_loader(loader: Loaders) -> LoaderType:
    loader = getattr(document_loaders, loader)
    return loader
