# Background worker for Cognexa backend

### Working principle

```mermaid

graph TD;
  A["Bun API (Render Web Service)"]-->B["Python Enqueue API (Render Web Service)"];
  B["Python Enqueue API (Render Web Service)"]-->C["Managed Redis (Render Redis OR Upstash)"];
  C["Managed Redis (Render Redis OR Upstash)"]-->D["Dramatiq Worker (Render Background Worker Service)"];
  D["Dramatiq Worker (Render Background Worker Service)"]-->E["Managed Postgres (Render Postgres)"];
  E["Managed Postgres (Render Postgres)"]-->F["Storage (S3 capable)"];
```

# How to run
>
> First of all you need docker to use redis
So run this in ur terminal

```
docker run -d \
--name redis \
-p 6379:6379 \
redis:7
```

This makes ur redis running on `redis://localhost:6379`
now set the env variales as in [config.py](config.py)
then :point_down:
> run [main.py](main.py)
> run `uvicorn api:app --host 0.0.0.0 --port 5001 --reload` in a separate terminal for the api
<details>
<summary>Future implementation</summary>
  - [ ] Multiple type of embeddings support
  - [ ] Semantic search capabale embeddings
  - [ ] Rewritten in GO
</details>

> [!WARNING]
> Ofcourse use doppler for the env variables

> [!CAUTION]
> Just don't do anything without knowing what u r doing , it's not very much commented

> [!NOTE]
> First checkout the [schema.sql](schema.sql)
