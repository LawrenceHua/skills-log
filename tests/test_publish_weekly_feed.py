from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "publish_weekly_feed.py"
SPEC = importlib.util.spec_from_file_location("publish_weekly_feed", SCRIPT)
assert SPEC and SPEC.loader
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class PublishWeeklyFeedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "skills" / "existing").mkdir(parents=True)
        (self.root / "skills" / "existing" / "SKILL.md").write_text(
            "---\nname: existing\ndescription: Existing source.\n---\n\n## When to use\nUse it for existing work.\n",
            encoding="utf-8",
        )
        (self.root / "skills.json").write_text(
            json.dumps(
                {
                    "updated": "2026-09-06",
                    "weeks": [
                        {
                            "week": "2026-W37",
                            "date": "2026-09-06",
                            "skills": [
                                {
                                    "name": "existing",
                                    "slug": "existing",
                                    "description": "Existing source.",
                                    "useFor": "Use it for existing work.",
                                    "path": "skills/existing",
                                }
                            ],
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_skill(self, slug: str, *, when_to_use: str | None = "Use it for new work.") -> None:
        body = "\n## Details\nSource details.\n"
        if when_to_use is not None:
            body = f"\n## When to use\n{when_to_use}\n" + body
        path = self.root / "skills" / slug
        path.mkdir()
        (path / "SKILL.md").write_text(
            f"---\nname: {slug}\ndescription: A real source description.\n---\n{body}",
            encoding="utf-8",
        )

    def test_no_new_source_fails_without_fabricating_week(self) -> None:
        before = (self.root / "skills.json").read_text(encoding="utf-8")
        with self.assertRaisesRegex(publisher.FeedError, "refusing to fabricate"):
            publisher.publish_feed(self.root, date(2026, 9, 20), today=date(2026, 9, 20))
        self.assertEqual(before, (self.root / "skills.json").read_text(encoding="utf-8"))

    def test_unqualified_source_fails_instead_of_fabricating_use_for(self) -> None:
        self.add_skill("missing-use", when_to_use=None)
        with self.assertRaisesRegex(publisher.FeedError, "missing-use"):
            publisher.publish_feed(self.root, date(2026, 9, 20), today=date(2026, 9, 20))

    def test_success_uses_source_and_is_idempotently_rejected(self) -> None:
        self.add_skill("real-new-skill")
        output, slugs = publisher.publish_feed(self.root, date(2026, 9, 20), write=True, today=date(2026, 9, 20))
        self.assertEqual(slugs, ["real-new-skill"])
        self.assertEqual(output["updated"], "2026-09-20")
        self.assertEqual(output["weeks"][0]["week"], "2026-W38")
        self.assertEqual(output["weeks"][0]["skills"][0]["useFor"], "Use it for new work.")
        with self.assertRaisesRegex(publisher.FeedError, "already published"):
            publisher.publish_feed(self.root, date(2026, 9, 20), today=date(2026, 9, 20))

    def test_duplicate_feed_slug_is_rejected(self) -> None:
        feed = json.loads((self.root / "skills.json").read_text(encoding="utf-8"))
        feed["weeks"][0]["skills"].append(feed["weeks"][0]["skills"][0].copy())
        (self.root / "skills.json").write_text(json.dumps(feed), encoding="utf-8")
        with self.assertRaisesRegex(publisher.FeedError, "duplicate published"):
            publisher.publish_feed(self.root, date(2026, 9, 13), today=date(2026, 9, 20))

    def test_non_sunday_and_backdated_dates_are_rejected(self) -> None:
        self.add_skill("real-new-skill")
        with self.assertRaisesRegex(publisher.FeedError, "Sunday"):
            publisher.publish_feed(self.root, date(2026, 9, 14), today=date(2026, 9, 20))
        with self.assertRaisesRegex(publisher.FeedError, "newer"):
            publisher.publish_feed(self.root, date(2026, 8, 30), today=date(2026, 9, 20))


if __name__ == "__main__":
    unittest.main()
