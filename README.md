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

Edit `config/default.yml` with your API credentials and desired streamers.
Credentials are defined under the ``credentials`` section and individual
streams specify a ``platform`` (``twitch`` or ``youtube``), a ``username`` or
channel ID and an optional ``quality`` setting.

## Web Interface

You can edit the configuration using a small Flask web interface. After
installing the dependencies, start the server:

```bash
python -m src.webapp
```

Open `http://localhost:8000` in your browser to update credentials and the list
of streams.

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
