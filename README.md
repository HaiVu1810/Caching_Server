# Caching Server

Simple FastAPI-based caching proxy server. Requests to the proxy are forwarded to an origin URL and responses are cached in local JSON files under `cache/`.

## Project structure

- `caching_server.py`: CLI entrypoint with `--port` and `--url` arguments.
- `Socket_server.py`: Sets `ORIGIN_URL` environment variable and starts uvicorn.
- `Fetchinghandle.py`: FastAPI app implementing caching proxy logic.
- `cache/`: JSON cache files are written here (e.g. `products.json`, `users.json`).
- `setup.py`: packaging entry point `caching-server=caching_server:main`.

## Requirements

- Python 3.8+
- `fastapi`
- `uvicorn`
- `requests`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

If you don't have `requirements.txt`, run:

```bash
python -m pip install fastapi uvicorn requests
```

## Usage

Run via package entry point (after install):

```bash
caching-server --port 8000 --url https://dummyjson.com
```

Or run directly:

```bash
python caching_server.py --port 8000 --url https://dummyjson.com
```

Then send requests:

```bash
curl http://localhost:8000/products
curl http://localhost:8000/products/1
curl http://localhost:8000/users
```

- first request: cache miss => fetch from origin + save cache
- subsequent request for same cache key: cache hit => read from `cache/<key>.json` and return

## What it does

- If `GET /{path}` is requested, builds origin URL using `ORIGIN_URL` plus `path`.
- Cache file key: first segment of path (e.g., `products` -> `cache/products.json`).
- Caches response JSON once then reuses for later hits.
- Adds `X-Cache` header with `Miss` or `Hit`.

## Notes

- This implementation is proof-of-concept and has no cache invalidation or concurrency locking.
- For production use, add error handling, TTL, locking, path normalization and streaming support.

## Development

Run source with reload for development:

```bash
uvicorn Fetchinghandle:app --host localhost --port 8000 --reload
```

Or through the app as above using `caching_server.py`.
