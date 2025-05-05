from typing import Union, Literal
from enum import Enum
from langchain_community.document_loaders import GitLoader, DirectoryLoader, RecursiveUrlLoader
from langchain_community import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings

LoaderType = Union[GitLoader, DirectoryLoader, RecursiveUrlLoader]

class DataLoaders(Enum):
    URL = "RecursiveUrlLoader"
    GIT = "GitLoader"
    LOCALDIR = "DirectoryLoader"


def get_data_loader(loader_name: str) -> LoaderType:
    loader = getattr(document_loaders, loader_name)
    return loader


def determine_loader(source_type: Literal["file", "repo", "url"]):
    if source_type == "repo":
        return get_data_loader(DataLoaders.GIT.value)
    elif source_type == "file":
        return get_data_loader(DataLoaders.LOCALDIR.value)
    elif source_type == "url":
        return get_data_loader(DataLoaders.URL.value)
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")
