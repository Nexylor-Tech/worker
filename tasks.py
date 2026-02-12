import dramatiq
from dramatiq.brokers.redis import RedisBroker
from config import Config
from db import get_db_cursor
from chunking import chunk_text
from embeddings import generate_embedding_batch
from storage import download_file_content

dramatiq.set_broker(RedisBroker(url=Config.REDIS_URL))


@dramatiq.actor(time_limit=300_000, max_retries=3, queue_name="default")
def process_file(file_id: str, project_id: str, storage_key: str):
    print(f"Processing task for File ID: {file_id}, Key: {storage_key}")
    try:
        with get_db_cursor() as (conn, cur):
            cur.execute(
                "UPDATE file SET status = %s WHERE id = %s", ("processing", file_id)
            )
        print(f"Downloading from S3: {storage_key}...")
        content = download_file_content(storage_key)
        chunks = chunk_text(content, chunk_size=800, overlap=100)
        print(f"Generated {len(chunks)} chunks")
        if not chunks:
            with get_db_cursor() as (conn, cur):
                cur.execute(
                    "UPDATE file SET status = 'ready' WHERE id = %s", (file_id,)
                )
            return
        batch_size = 100
        vectors = []
        for i in range(0, len(chunks), batch_size):
            batch_texts = chunks[i : i + batch_size]
            batch_vectors = generate_embedding_batch(batch_texts)
            vectors.extend(batch_vectors)
        with get_db_cursor() as (conn, cur):
            with conn.transaction():
                cur.execute(
                    "DELETE FROM knowledge_chunks WHERE file_id = %s", (file_id,)
                )
                data_to_insert = [
                    (project_id, file_id, chunk, vector)
                    for chunk, vector in zip(chunks, vectors)
                ]
                cur.executemany(
                    """
                    INSERT INTO knowledge_chunks (project_id, file_id, content, embedding) VALUES (%s, %s, %s, %s)
                    """,
                    data_to_insert,
                )
                cur.execute(
                    "UPDATE file SET status = 'ready' WHERE id = %s",
                    (file_id,),
                )
        print(f"File {file_id}: Success.")

    except Exception as e:
        print(f"File {file_id}: Failed. Error: {e}")
        try:
            with get_db_cursor() as (conn, cur):
                cur.execute(
                    "UPDATE file SET status = 'failed' WHERE id = %s", (file_id,)
                )
        except Exception:
            pass
        raise e
