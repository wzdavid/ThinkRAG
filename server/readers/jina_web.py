from typing import List, Optional, Dict, Callable
from datetime import datetime

import requests, re
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document


class JinaWebReader(BasePydanticReader):
    """Jina web page reader.

    Reads pages from the web.

    """

    def __init__(self) -> None:
        """Initialize with parameters."""

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []
        for url in urls:
            new_url = "https://r.jina.ai/" + url
            response = requests.get(new_url)
            text = response.text

            # Extract Title
            title_match = re.search(r"Title:\s*(.*)", text)
            title = title_match.group(1) if title_match else None

            # Extract URL Source
            url_match = re.search(r"URL Source:\s*(.*)", text)
            url_source = url_match.group(1) if url_match else None

            # Extract Markdown Content
            markdown_match = re.search(r"Markdown Content:\s*(.*)", text, re.DOTALL)
            markdown_content = markdown_match.group(1).strip() if markdown_match else None

            # Compose metadata
            metadata: Dict = {
                "title": title,
                "url_source": url_source,
                "creation_date": datetime.now().date().isoformat(),  # Convert datetime to ISO format string
            }

            documents.append(Document(text=markdown_content, id_=url, metadata=metadata or {}))

        return documents
