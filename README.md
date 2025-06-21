# stream-to-shorts

A minimal system for monitoring Twitch streams and creating short clips. This
repository provides a simple skeleton with pluggable modules. It is **not** a
fully featured production system but serves as a starting point for further
development.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit `config/default.yml` with your Twitch API credentials and desired
streamers.

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
