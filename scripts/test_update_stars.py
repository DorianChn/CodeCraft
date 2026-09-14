import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("update_stars.py")
SPEC = importlib.util.spec_from_file_location("update_stars", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class UpdateStarsTests(unittest.TestCase):
    def test_trending_uses_moving_window(self):
        with patch.object(MODULE, "github_request", return_value={"items": []}) as request:
            MODULE.fetch_trending(since="weekly")

        url = request.call_args.args[0]
        self.assertIn(f"pushed:>{MODULE.recent_date(days=7)}", url)
        self.assertNotIn("2025-01-01", url)

    def test_generated_label_reports_total_stars(self):
        output = MODULE.generate_stars_js([
            {
                "full_name": "demo/project",
                "stargazers_count": 1234,
                "description": "demo",
                "language": "Python",
                "topics": [],
                "html_url": "https://github.com/demo/project",
            }
        ])

        self.assertEqual(output[0]["stars"], "1,234 stars")
        self.assertNotIn("/周", output[0]["stars"])


if __name__ == "__main__":
    unittest.main()
