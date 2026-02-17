from google import genai
from google.genai import types
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)


def generate_embedding_batch(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
        ),
    )
    embedding = result.embeddings
    if not embedding:
        raise ValueError("No embeddings returned")

    if isinstance(embedding, list):
        results = []
        for e in embedding:
            if isinstance(e, dict):
                if "values" in e:
                    results.append(e["values"])
                elif "embedding" in e:
                    results.append(e["embedding"])
                else:
                    results.append(e)
            elif hasattr(e, "values"):
                results.append(e.values)
            else:
                results.append(e)
        return results

    if isinstance(embedding, dict):
        return [embedding.get("values", embedding.get("embedding"))]

    raise ValueError("Unexpected embedding response format")
