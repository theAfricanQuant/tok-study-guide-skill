#!/usr/bin/env python3
"""Fetch a YouTube transcript, timestamped cues, and video metadata.

Authenticated cookies are optional and must stay on the user's trusted local
machine. Never send a logged-in cookie jar to a hosted agent or ask a user to
upload one.

Usage:
    python3 fetch_transcript.py <youtube-url-or-id> [--out /tmp/transcript.txt]
    python3 fetch_transcript.py <url> --cookies-from-browser chrome
    python3 fetch_transcript.py <url> --cookies /path/to/local/cookies.txt

Writes the clean transcript, a timestamped cue sidecar, and metadata JSON.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request


def video_id(value: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", value)
    if match:
        return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    sys.exit(f"Could not find a YouTube video id in: {value}")


def ensure(package: str, import_name: str | None = None) -> None:
    try:
        __import__(import_name or package)
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", package,
             "--break-system-packages"],
            check=False,
        )


def oembed(video: str) -> dict:
    """Fetch public title/channel metadata using normal TLS verification."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video}&format=json"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = json.load(response)
            return {"title": data.get("title", ""), "channel": data.get("author_name", "")}
    except Exception:
        return {"title": "", "channel": ""}


def clean_caption(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = (text.replace("&gt;&gt;", "|").replace("&nbsp;", " ").replace("&amp;", "&")
            .replace("&gt;", ">").replace("&lt;", "<").replace("&#39;", "'")
            .replace("&quot;", '"'))
    return re.sub(r"\s+", " ", text).strip()


def clean_vtt(text: str) -> str:
    lines, previous = [], ""
    for line in text.splitlines():
        if "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")) or not line.strip():
            continue
        cue = clean_caption(line)
        if cue and cue != previous:
            lines.append(cue)
            previous = cue
    # Auto-captions often roll forward by repeating the previous cue plus new words.
    merged = []
    for cue in lines:
        if merged and cue.startswith(merged[-1]):
            merged[-1] = cue
        elif not merged or cue not in merged[-1]:
            merged.append(cue)
    return re.sub(r"\s+", " ", " ".join(merged)).strip()


VTT_TIME = re.compile(r"(?:(\d+):)?([0-5]?\d):([0-5]?\d)[.,](\d{3})")


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def timestamped_vtt(text: str) -> str:
    """Keep each cleaned VTT cue beside its start time for source citations."""
    cues, previous = [], None
    for block in re.split(r"\n\s*\n", text):
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        match = VTT_TIME.search(lines[timing_index])
        if not match:
            continue
        hours = int(match.group(1) or 0)
        minutes, seconds, millis = (int(match.group(i)) for i in (2, 3, 4))
        start = hours * 3600 + minutes * 60 + seconds + millis / 1000
        cue = clean_caption(" ".join(lines[timing_index + 1:]))
        if cue and cue != previous:
            cues.append(f"[{format_timestamp(start)}] {cue}")
            previous = cue
    return "\n".join(cues)


PLAYER_CLIENTS = [None, "web_embedded", "web_safari", "mweb", "tv", "android"]
LANGUAGES = ("en-orig", "en", "en.*")
BOT_WALL_MARKERS = (
    "sign in to confirm", "login_required", "requestblocked", "ipblocked", "not a bot",
)
AUTH_COOKIE_NAMES = {
    "SID", "__Secure-1PSID", "__Secure-3PSID", "HSID", "SSID", "APISID", "SAPISID",
    "LOGIN_INFO",
}
DIAGNOSTICS = {"walled": False, "cookies_used": False, "attempts": 0}


def iter_netscape_cookie_rows(cookie_path: str):
    """Yield Netscape cookie columns, including records prefixed with #HttpOnly_."""
    with open(cookie_path, encoding="utf-8", errors="replace") as cookie_file:
        for line in cookie_file:
            if line.startswith("#HttpOnly_"):
                line = line[len("#HttpOnly_"):]
            elif line.startswith("#") or not line.strip():
                continue
            fields = line.rstrip("\r\n").split("\t")
            if len(fields) >= 7:
                yield fields[:7]


def cookie_names(cookie_path: str) -> list[str]:
    try:
        return [row[5] for row in iter_netscape_cookie_rows(cookie_path)]
    except OSError:
        return []


def warn_if_anonymous(cookie_path: str) -> None:
    names = set(cookie_names(cookie_path))
    if not names.intersection(AUTH_COOKIE_NAMES):
        print(
            "[cookies] WARNING: this file has no recognized YouTube login cookies; "
            "it may be an anonymous export.",
            file=sys.stderr,
        )


def warn_if_exposed(cookie_path: str) -> None:
    """Warn about overly broad POSIX permissions without changing the user's file."""
    if os.name != "posix":
        return
    try:
        mode = os.stat(cookie_path).st_mode & 0o777
    except OSError:
        return
    if mode & 0o077:
        print(
            f"[cookies] WARNING: {cookie_path} is readable or writable by group/others; "
            "restrict it with chmod 600.",
            file=sys.stderr,
        )


def resolve_options(cookie_arg, browser_arg, client_args, environ=None):
    environ = os.environ if environ is None else environ
    cookie_path = cookie_arg or environ.get("YT_DLP_COOKIES") or None
    browser = browser_arg or environ.get("YT_DLP_COOKIES_FROM_BROWSER") or None
    if cookie_path:
        cookie_path = os.path.expanduser(cookie_path)
    if cookie_path and browser:
        raise ValueError("Choose --cookies or --cookies-from-browser, not both.")
    if cookie_path and not os.path.isfile(cookie_path):
        raise ValueError(f"Cookie file not found: {cookie_path}")

    if client_args is None:
        client_args = [
            client.strip()
            for client in environ.get("YT_DLP_PLAYER_CLIENT", "").split(",")
            if client.strip()
        ]
    clients = [None if client == "default" else client for client in client_args] or None
    return cookie_path, browser, clients


def build_ytdlp_command(video: str, output_template: str, language: str,
                        client: str | None, cookie_path: str | None = None,
                        browser: str | None = None) -> list[str]:
    """Build an authenticated or anonymous yt-dlp command with TLS checks enabled."""
    if cookie_path and browser:
        raise ValueError("Choose one local cookie source, not both.")
    command = [
        sys.executable, "-m", "yt_dlp", "--skip-download", "--ignore-no-formats-error",
        "--write-auto-subs", "--write-subs", "--sub-langs", language, "--sub-format", "vtt",
        "--sleep-subtitles", "2", "-o", output_template,
    ]
    if cookie_path:
        command += ["--cookies", cookie_path]
    elif browser:
        command += ["--cookies-from-browser", browser]
    if client:
        command += ["--extractor-args", f"youtube:player_client={client}"]
    command.append(f"https://www.youtube.com/watch?v={video}")
    return command


def is_bot_wall(message) -> bool:
    detail = f"{type(message).__name__}: {message}".lower()
    return any(marker in detail for marker in BOT_WALL_MARKERS)


def via_ytdlp(video: str, cookie_path: str | None = None, browser: str | None = None,
              clients: list[str | None] | None = None) -> tuple[str, str] | None:
    """Try the chosen/default player clients, keeping certificate validation enabled."""
    if cookie_path and browser:
        raise ValueError("Choose one local cookie source, not both.")
    ensure("yt-dlp", "yt_dlp")
    ensure("curl_cffi")
    DIAGNOSTICS["cookies_used"] = bool(cookie_path or browser)
    client_order = PLAYER_CLIENTS if clients is None else clients

    for client in client_order:
        client_blocked = False
        for language in LANGUAGES:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_template = os.path.join(temp_dir, "video")
                command = build_ytdlp_command(
                    video, output_template, language, client, cookie_path, browser,
                )
                result = subprocess.run(command, capture_output=True, text=True)
                subtitle_files = sorted(glob.glob(os.path.join(temp_dir, "video*.vtt")))
                if subtitle_files:
                    with open(subtitle_files[0], encoding="utf-8", errors="replace") as subtitle:
                        raw = subtitle.read()
                    readable = clean_vtt(raw)
                    if len(readable) > 200:
                        print(
                            f"[yt-dlp] subtitles via client={client or 'default'} "
                            f"language={language}",
                            file=sys.stderr,
                        )
                        return readable, timestamped_vtt(raw)

                response = f"{result.stderr or ''}\n{result.stdout or ''}"
                DIAGNOSTICS["attempts"] += 1
                if is_bot_wall(response):
                    DIAGNOSTICS["walled"] = True
                    client_blocked = True
                    break  # Skip remaining language variants; continue with the next client.
                if "429" in response:
                    time.sleep(15)
        if client_blocked:
            continue
    return None


def via_api(video: str) -> tuple[str, str] | None:
    """Unauthenticated fallback; session cookies are deliberately not forwarded."""
    ensure("youtube-transcript-api", "youtube_transcript_api")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi().fetch(video)
        segments = []
        for item in transcript:
            text = clean_caption(item.text)
            start = float(item.start)
            if text:
                segments.append((start, text))
        readable = re.sub(r"\s+", " ", " ".join(text for _, text in segments)).strip()
        timed = "\n".join(f"[{format_timestamp(start)}] {text}" for start, text in segments)
        return readable, timed
    except Exception as error:
        if is_bot_wall(error):
            DIAGNOSTICS["walled"] = True
        return None


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript. Local browser cookies are optional; never upload them."
    )
    parser.add_argument("video")
    parser.add_argument("--out", default="/tmp/transcript.txt")
    auth = parser.add_mutually_exclusive_group()
    auth.add_argument(
        "--cookies", metavar="FILE",
        help="local Netscape cookie file (env: YT_DLP_COOKIES); treat as an account credential",
    )
    auth.add_argument(
        "--cookies-from-browser", metavar="BROWSER",
        help="read a local browser profile, e.g. chrome (env: YT_DLP_COOKIES_FROM_BROWSER)",
    )
    parser.add_argument(
        "--player-client", action="append", default=None, metavar="CLIENT",
        help="player client to try, repeatable and ordered (env: YT_DLP_PLAYER_CLIENT)",
    )
    return parser


def main(argv=None) -> None:
    args = make_parser().parse_args(argv)
    try:
        cookie_path, browser, clients = resolve_options(
            args.cookies, args.cookies_from_browser, args.player_client,
        )
    except ValueError as error:
        sys.exit(str(error))

    DIAGNOSTICS.update(walled=False, cookies_used=False, attempts=0)
    if cookie_path:
        print("[cookies] Reading a local cookie file; cookie values are never logged.", file=sys.stderr)
        warn_if_anonymous(cookie_path)
        warn_if_exposed(cookie_path)
    if browser:
        print(f"[cookies] Reading the local {browser} browser profile; cookie values are never logged.",
              file=sys.stderr)

    video = video_id(args.video)
    metadata = {"id": video, "url": f"https://www.youtube.com/watch?v={video}", **oembed(video)}
    result = via_ytdlp(video, cookie_path, browser, clients) or via_api(video)
    if not result or not result[0]:
        if DIAGNOSTICS["walled"]:
            message = ["YouTube blocked transcript access in this environment."]
            if DIAGNOSTICS["cookies_used"]:
                message.append(
                    "The selected local cookie source did not clear the block; check that it is "
                    "signed in and current. Keep cookie values on this trusted machine."
                )
            else:
                message.append(
                    "Do not upload browser cookies or cookie files to an agent. If running this "
                    "script locally, rerun it there with --cookies-from-browser chrome; otherwise "
                    "provide a transcript or captions."
                )
        else:
            message = ["No transcript could be fetched. Ask for a transcript or usable captions."]
        sys.exit(" ".join(message))

    readable, timed_cues = result
    with open(args.out, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(readable)
    timestamped_path = args.out + ".timestamps.txt"
    with open(timestamped_path, "w", encoding="utf-8") as timestamped_file:
        timestamped_file.write(timed_cues)
    metadata.update(
        chars=len(readable), words=len(readable.split()), timestamped_transcript=timestamped_path,
    )
    with open(args.out + ".meta.json", "w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)
    print(json.dumps(metadata, indent=2))
    print(
        f"\nTranscript saved to {args.out}; timestamped cues saved to {timestamped_path}. "
        "Read it fully in ~40,000-character chunks before writing."
    )


if __name__ == "__main__":
    main()
