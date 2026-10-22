#!/usr/bin/env python3
"""Fetch a YouTube video's title and transcript as clean plain text.

Usage:
    python3 fetch_transcript.py <youtube-url-or-id> [--out /tmp/transcript.txt]

Writes:
    <out>                   cleaned transcript for reading
    <out>.timestamps.txt    cleaned caption cues, each with a [HH:MM:SS] anchor
    <out>.meta.json         video metadata and transcript counts

Strategy (first one that works wins):
    1. yt-dlp auto/manual English subtitles (VTT), with certificate checks off
       (sandboxes often sit behind a TLS-inspecting proxy).
    2. youtube-transcript-api (often blocked from cloud IPs, but worth a try).
If both fail, the script exits non-zero and tells you to ask the user to paste
or upload the transcript instead.
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
import ssl


def video_id(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    sys.exit(f"Could not find a YouTube video id in: {s}")


def ensure(pkg: str, import_name: str | None = None):
    try:
        __import__(import_name or pkg)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg,
                        "--break-system-packages"], check=False)


def oembed(vid: str) -> dict:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=20) as r:
            d = json.load(r)
            return {"title": d.get("title", ""), "channel": d.get("author_name", "")}
    except Exception:
        return {"title": "", "channel": ""}


def clean_caption(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = (text.replace("&gt;&gt;", "|").replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&gt;", ">").replace("&lt;", "<").replace("&#39;", "'").replace("&quot;", '"'))
    return re.sub(r"\s+", " ", text).strip()


def clean_vtt(text: str) -> str:
    out, prev = [], ""
    for line in text.splitlines():
        if "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")) or not line.strip():
            continue
        t = clean_caption(line)
        if t and t != prev:
            out.append(t)
            prev = t
    # Auto-captions roll: each cue often repeats the previous one plus new words.
    merged = []
    for t in out:
        if merged and t.startswith(merged[-1]):
            merged[-1] = t
        elif not merged or t not in merged[-1]:
            merged.append(t)
    return re.sub(r"\s+", " ", " ".join(merged)).strip()


VTT_TIME = re.compile(r"(?:(\d+):)?([0-5]?\d):([0-5]?\d)[.,](\d{3})")


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def timestamped_vtt(text: str) -> str:
    """Keep cleaned VTT cue text next to each cue's start time for citations."""
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
        minutes, seconds, millis = int(match.group(2)), int(match.group(3)), int(match.group(4))
        start = hours * 3600 + minutes * 60 + seconds + millis / 1000
        cue = clean_caption(" ".join(lines[timing_index + 1:]))
        if cue and cue != previous:
            cues.append(f"[{format_timestamp(start)}] {cue}")
            previous = cue
    return "\n".join(cues)


PLAYER_CLIENTS = [None, "web_embedded", "web_safari", "mweb", "tv", "android"]


def via_ytdlp(vid: str) -> tuple[str, str] | None:
    """Try yt-dlp with several YouTube player clients.

    YouTube sometimes answers sandbox IPs with "Sign in to confirm you're not a bot"
    for the default client while another client (often web_embedded) still serves
    subtitles, so we cycle through them.
    """
    ensure("yt-dlp", "yt_dlp")
    ensure("curl_cffi")  # lets yt-dlp impersonate a browser; avoids many HTTP 429s
    # Requesting one track at a time ("en-orig" first) also avoids 429 Too Many Requests,
    # which YouTube often returns when several subtitle tracks are fetched back to back.
    for attempt, (client, langs) in enumerate(
            [(c, l) for c in PLAYER_CLIENTS for l in ("en-orig", "en", "en.*")]):
        tmp = tempfile.mkdtemp()
        cmd = [sys.executable, "-m", "yt_dlp", "--no-check-certificates", "--skip-download",
               "--ignore-no-formats-error", "--write-auto-subs", "--write-subs",
               "--sub-langs", langs, "--sub-format", "vtt", "--sleep-subtitles", "2",
               "-o", os.path.join(tmp, "v")]
        if client:
            cmd += ["--extractor-args", f"youtube:player_client={client}"]
        cmd.append(f"https://www.youtube.com/watch?v={vid}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        files = glob.glob(os.path.join(tmp, "v*.vtt"))
        if files:
            files.sort(key=lambda f: len(f))
            raw = open(files[0], encoding="utf-8", errors="ignore").read()
            text = clean_vtt(raw)
            cues = timestamped_vtt(raw)
            if len(text) > 200:
                print(f"[yt-dlp] subtitles via client={client or 'default'} langs={langs}", file=sys.stderr)
                return text, cues
        if "429" in (r.stderr + r.stdout):
            time.sleep(15)  # back off before the next attempt
    return None


def via_api(vid: str) -> tuple[str, str] | None:
    ensure("youtube-transcript-api", "youtube_transcript_api")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi().fetch(vid)
        segments = []
        for item in transcript:
            text = clean_caption(item.text)
            start = float(item.start)
            if text:
                segments.append((start, text))
        readable = re.sub(r"\s+", " ", " ".join(text for _, text in segments)).strip()
        timed = "\n".join(f"[{format_timestamp(start)}] {text}" for start, text in segments)
        return readable, timed
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="/tmp/transcript.txt")
    a = ap.parse_args()
    vid = video_id(a.video)
    meta = {"id": vid, "url": f"https://www.youtube.com/watch?v={vid}", **oembed(vid)}
    result = via_ytdlp(vid) or via_api(vid)
    if not result:
        sys.exit("No transcript could be fetched. Ask the user to paste or upload the transcript.")
    text, timed_cues = result
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    timestamped_path = a.out + ".timestamps.txt"
    with open(timestamped_path, "w", encoding="utf-8") as f:
        f.write(timed_cues)
    meta.update(chars=len(text), words=len(text.split()), timestamped_transcript=timestamped_path)
    with open(a.out + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))
    print(f"\nTranscript saved to {a.out}; timestamped cues saved to {timestamped_path}. Read the transcript fully in ~40,000-character chunks before writing.")


if __name__ == "__main__":
    main()
