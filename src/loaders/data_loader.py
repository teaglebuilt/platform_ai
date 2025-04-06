from typing import Union
from enum import Enum
from langchain_community.document_loaders import GitLoader, DirectoryLoader, RecursiveUrlLoader
from langchain_community import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import LanceDB
import lancedb

LoaderType = Union[GitLoader, DirectoryLoader, RecursiveUrlLoader]

class DataLoaders(Enum):
    URL = "RecursiveUrlLoader"
    GIT = "GitLoader"
    LOCALDIR = "DirectoryLoader"


def get_data_loader(loader_name: str) -> LoaderType:
    loader = getattr(document_loaders, loader_name)
    return loader
