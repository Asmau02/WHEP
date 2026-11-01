from pathlib import Path
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db_v2"
COLLECTION_NAME = "whep_health_sources_clean"

def get_collection():
    if not CHROMA_PATH.exists() or not any(CHROMA_PATH.iterdir()):
        raise FileNotFoundError(
            f"ChromaDB data was not found in: {CHROMA_PATH}. "
            "Copy your existing chroma_db_v2 folder into the WHEP project folder."
        )
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_collection(name=COLLECTION_NAME)

def retrieve_context(question, n_results=3):
    collection = get_collection()
    result = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    context_parts = []
    sources = []
    seen_urls = set()

    for index, document in enumerate(documents):
        metadata = metadatas[index] or {}
        title = metadata.get("title", "WHEP knowledge-base source")
        raw_url = metadata.get("url", "")
        url = raw_url

        # Some stored URLs are Markdown links, e.g. [https://...](https://...)
        if "](" in raw_url and raw_url.endswith(")"):
            url = raw_url.rsplit("](", 1)[-1][:-1]

        distance = distances[index] if index < len(distances) else None
        context_parts.append(
            f"Source: {title}\n"
            f"URL: {url}\n"
            f"Retrieved distance: {distance}\n"
            f"Content:\n{document}"
        )

        if url and url not in seen_urls:
            sources.append({"title": title, "url": url})
            seen_urls.add(url)

    context = "\n\n---\n\n".join(context_parts)
    return context, sources
