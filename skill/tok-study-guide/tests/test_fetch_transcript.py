"""Offline unit tests for transcript fetching and local cookie handling."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_transcript.py"
SPEC = importlib.util.spec_from_file_location("fetch_transcript", SCRIPT_PATH)
fetch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetch)


class FetchTranscriptTests(unittest.TestCase):
    def setUp(self):
        fetch.DIAGNOSTICS.update(walled=False, cookies_used=False, attempts=0)

    def test_http_only_cookie_rows_are_recognized_without_reading_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cookie_file = Path(temp_dir) / "cookies.txt"
            cookie_file.write_text(
                "# Netscape HTTP Cookie File\n"
                "#HttpOnly_.youtube.com\tTRUE\t/\tTRUE\t0\tSID\tsecret-session-value\n"
                ".youtube.com\tTRUE\t/\tFALSE\t0\tPREF\tlang=en\n",
                encoding="utf-8",
            )
            self.assertEqual(fetch.cookie_names(str(cookie_file)), ["SID", "PREF"])

    def test_empty_cookie_file_warns_without_printing_cookie_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cookie_file = Path(temp_dir) / "empty.txt"
            cookie_file.write_text("# Netscape HTTP Cookie File\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                fetch.warn_if_anonymous(str(cookie_file))
            self.assertIn("no recognized YouTube login cookies", output.getvalue())
            self.assertNotIn("secret-session-value", output.getvalue())

    def test_auth_sources_are_mutually_exclusive_in_environment(self):
        env = {
            "YT_DLP_COOKIES": "/tmp/local-cookies.txt",
            "YT_DLP_COOKIES_FROM_BROWSER": "chrome",
        }
        with self.assertRaisesRegex(ValueError, "Choose --cookies or --cookies-from-browser"):
            fetch.resolve_options(None, None, None, env)

    def test_player_clients_keep_environment_order(self):
        _, _, clients = fetch.resolve_options(
            None, None, None, {"YT_DLP_PLAYER_CLIENT": "tv,mweb"},
        )
        self.assertEqual(clients, ["tv", "mweb"])

    def test_authenticated_command_keeps_tls_validation_enabled(self):
        command = fetch.build_ytdlp_command(
            "abcdefghijk", "/tmp/video", "en", "tv", cookie_path="/tmp/private.txt",
        )
        self.assertIn("--cookies", command)
        self.assertIn("/tmp/private.txt", command)
        self.assertIn("--extractor-args", command)
        self.assertNotIn("--no-check-certificates", command)
        self.assertNotIn("--cookies-from-browser", command)

    def test_client_after_bot_wall_is_still_tried(self):
        calls = []
        cue_text = "A useful transcript sentence for testing. " * 12
        vtt = "WEBVTT\n\n00:00:03.000 --> 00:00:07.000\n" + cue_text + "\n\n"

        def fake_run(command, capture_output, text):
            calls.append(command)
            client = None
            if "--extractor-args" in command:
                client = command[command.index("--extractor-args") + 1]
            if client and client.endswith("=tv"):
                return types.SimpleNamespace(stdout="", stderr="Sign in to confirm you're not a bot")
            output_template = command[command.index("-o") + 1]
            Path(output_template + ".en.vtt").write_text(vtt, encoding="utf-8")
            return types.SimpleNamespace(stdout="", stderr="")

        with mock.patch.object(fetch, "ensure"), \
             mock.patch.object(fetch.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(fetch.time, "sleep"):
            result = fetch.via_ytdlp(
                "abcdefghijk", cookie_path="/tmp/local.txt", clients=["tv", "mweb"],
            )

        self.assertIsNotNone(result)
        self.assertEqual(len(calls), 2)
        self.assertIn("youtube:player_client=tv", calls[0])
        self.assertIn("youtube:player_client=mweb", calls[1])
        self.assertTrue(fetch.DIAGNOSTICS["walled"])
        self.assertTrue(fetch.DIAGNOSTICS["cookies_used"])
        self.assertIn("[00:00:03]", result[1])
        self.assertTrue(all("--no-check-certificates" not in call for call in calls))

    def test_api_request_block_is_reported_as_a_bot_wall(self):
        class RequestBlocked(Exception):
            pass

        class FakeTranscriptApi:
            def fetch(self, _video):
                raise RequestBlocked("IP blocked")

        fake_module = types.SimpleNamespace(YouTubeTranscriptApi=FakeTranscriptApi)
        with mock.patch.object(fetch, "ensure"), \
             mock.patch.dict(sys.modules, {"youtube_transcript_api": fake_module}):
            self.assertIsNone(fetch.via_api("abcdefghijk"))
        self.assertTrue(fetch.DIAGNOSTICS["walled"])

    def test_main_writes_html_workflow_transcript_and_timestamp_sidecar(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = str(Path(temp_dir) / "video.txt")
            timed = "[00:00:03] A useful transcript sentence."
            with mock.patch.object(fetch, "via_ytdlp", return_value=("A useful transcript sentence.", timed)), \
                 mock.patch.object(fetch, "oembed", return_value={"title": "Example", "channel": "Channel"}), \
                 contextlib.redirect_stdout(io.StringIO()):
                fetch.main(["abcdefghijk", "--out", output])
            self.assertEqual(Path(output).read_text(encoding="utf-8"), "A useful transcript sentence.")
            self.assertEqual(Path(output + ".timestamps.txt").read_text(encoding="utf-8"), timed)
            self.assertTrue(Path(output + ".meta.json").exists())


if __name__ == "__main__":
    unittest.main()
