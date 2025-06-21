# stream-to-shorts

A minimal system for monitoring live streams and creating short clips. The
project started with Twitch support and now exposes a small abstraction layer so
additional platforms can be plugged in easily. It is **not** a fully featured
production system but serves as a starting point for further development.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit `config/default.yml` with your API credentials and desired streamers. Each
stream entry can specify a ``platform`` (``twitch`` or ``youtube``) and a
``username`` or channel ID.

## Running

```bash
python -m src
```

## Docker

Build and run using Docker:

```bash
docker build -f docker/Dockerfile -t stream-to-shorts .
docker run --rm stream-to-shorts
```
