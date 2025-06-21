from __future__ import annotations
"""Minimal Flask web interface to edit configuration."""

from pathlib import Path

import yaml
from flask import Flask, render_template_string, request, redirect, url_for


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Stream to Shorts Config</title>
  <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\">
</head>
<body class=\"p-4\">
  <div class=\"container\">
    <h1 class=\"mb-4\">Configuration</h1>
    <form method=\"post\">
      <h3>Credentials</h3>
      <div class=\"mb-3\">
        <label for=\"twitch_client_id\" class=\"form-label\">Twitch Client ID</label>
        <input type=\"text\" class=\"form-control\" id=\"twitch_client_id\" name=\"twitch_client_id\" value=\"{{ twitch_client_id }}\">
      </div>
      <div class=\"mb-3\">
        <label for=\"twitch_oauth_token\" class=\"form-label\">Twitch OAuth Token</label>
        <input type=\"text\" class=\"form-control\" id=\"twitch_oauth_token\" name=\"twitch_oauth_token\" value=\"{{ twitch_oauth_token }}\">
      </div>
      <div class=\"mb-3\">
        <label for=\"youtube_api_key\" class=\"form-label\">YouTube API Key</label>
        <input type=\"text\" class=\"form-control\" id=\"youtube_api_key\" name=\"youtube_api_key\" value=\"{{ youtube_api_key }}\">
      </div>
      <h3>Streams</h3>
      <div class=\"mb-3\">
        <label for=\"streams\" class=\"form-label\">One per line as platform:username:quality</label>
        <textarea class=\"form-control\" id=\"streams\" name=\"streams\" rows=\"4\">{{ streams_value }}</textarea>
      </div>
      <button type=\"submit\" class=\"btn btn-primary\">Save</button>
    </form>
  </div>
</body>
</html>
"""


def create_app(config_path: str = "config/default.yml") -> Flask:
    """Return a configured Flask application."""

    app = Flask(__name__)
    config_file = Path(config_path)

    def load_cfg() -> dict:
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}
        return {}

    def save_cfg(data: dict) -> None:
        with config_file.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh)

    @app.route("/", methods=["GET", "POST"])
    def index():
        cfg = load_cfg()
        if request.method == "POST":
            twitch_client_id = request.form.get("twitch_client_id", "").strip()
            twitch_oauth_token = request.form.get("twitch_oauth_token", "").strip()
            youtube_api_key = request.form.get("youtube_api_key", "").strip()
            streams_raw = request.form.get("streams", "")

            credentials = {}
            if twitch_client_id and twitch_oauth_token:
                credentials["twitch"] = {
                    "client_id": twitch_client_id,
                    "oauth_token": twitch_oauth_token,
                }
            if youtube_api_key:
                credentials["youtube"] = {"api_key": youtube_api_key}

            streams = []
            for line in streams_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(":")]
                if len(parts) >= 2:
                    platform = parts[0]
                    username = parts[1]
                    quality = parts[2] if len(parts) > 2 else "best"
                    streams.append({
                        "platform": platform,
                        "username": username,
                        "quality": quality,
                    })

            data = {
                "credentials": credentials,
                "streams": streams,
                "storage": cfg.get("storage", {"recordings": "recordings/", "database": "data.db"}),
                "scheduler": cfg.get("scheduler", {"interval": 60}),
            }
            save_cfg(data)
            return redirect(url_for("index"))

        twitch_client_id = cfg.get("credentials", {}).get("twitch", {}).get("client_id", "")
        twitch_oauth_token = cfg.get("credentials", {}).get("twitch", {}).get("oauth_token", "")
        youtube_api_key = cfg.get("credentials", {}).get("youtube", {}).get("api_key", "")
        streams_lines = []
        for stream in cfg.get("streams", []):
            platform = stream.get("platform", "")
            username = stream.get("username", "")
            quality = stream.get("quality", "best")
            streams_lines.append(f"{platform}:{username}:{quality}")
        streams_value = "\n".join(streams_lines)

        return render_template_string(
            HTML_TEMPLATE,
            twitch_client_id=twitch_client_id,
            twitch_oauth_token=twitch_oauth_token,
            youtube_api_key=youtube_api_key,
            streams_value=streams_value,
        )

    return app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
