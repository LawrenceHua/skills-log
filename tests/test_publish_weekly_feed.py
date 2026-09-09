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

    def test_legacy_sunday_batches_use_the_following_monday_iso_week(self) -> None:
        self.assertEqual(publisher._week_id(date(2026, 9, 6)), "2026-W37")
        self.assertEqual(publisher._week_id(date(2026, 7, 12)), "2026-W29")

    def test_unqualified_source_fails_instead_of_fabricating_use_for(self) -> None:
        self.add_skill("missing-use", when_to_use=None)
        with self.assertRaisesRegex(publisher.FeedError, "missing-use"):
            publisher.publish_feed(self.root, date(2026, 9, 20), today=date(2026, 9, 20))

    def test_success_uses_source_and_same_date_rerun_is_unchanged(self) -> None:
        self.add_skill("real-new-skill")
        output, slugs = publisher.publish_feed(self.root, date(2026, 9, 13), write=True, today=date(2026, 9, 13))
        self.assertEqual(slugs, ["real-new-skill"])
        self.assertEqual(output["updated"], "2026-09-13")
        self.assertEqual(output["weeks"][0]["week"], "2026-W38")
        self.assertEqual(output["weeks"][0]["skills"][0]["useFor"], "Use it for new work.")
        before = (self.root / "skills.json").read_text(encoding="utf-8")
        rerun, rerun_slugs = publisher.publish_feed(self.root, date(2026, 9, 13), today=date(2026, 9, 13), write=True)
        self.assertEqual(rerun_slugs, [])
        self.assertEqual(rerun, output)
        self.assertEqual(before, (self.root / "skills.json").read_text(encoding="utf-8"))

    def test_same_date_rerun_is_unchanged_when_sources_are_already_published(self) -> None:
        before = (self.root / "skills.json").read_text(encoding="utf-8")
        output, slugs = publisher.publish_feed(self.root, date(2026, 9, 6), today=date(2026, 9, 6))
        self.assertEqual(slugs, [])
        self.assertEqual(output["updated"], "2026-09-06")
        self.assertEqual(before, (self.root / "skills.json").read_text(encoding="utf-8"))

    def test_same_date_with_new_source_remains_a_conflict(self) -> None:
        self.add_skill("real-new-skill")
        with self.assertRaisesRegex(publisher.FeedError, "already published"):
            publisher.publish_feed(self.root, date(2026, 9, 6), today=date(2026, 9, 6))

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

    def test_malformed_or_non_string_descriptions_cannot_enter_feed(self) -> None:
        self.add_skill("new-source")
        source = self.root / "skills" / "new-source" / "SKILL.md"
        before = (self.root / "skills.json").read_bytes()
        for description in (
            '[unterminated', '"unterminated', "'unterminated", '"bad\\q escape"',
            '"valid" trailing', '"\\ud800"', 'null', '~', 'true', 'yes', '123', '.5e3', '[one, two]',
            '{key: value}', '>\n  Folded text.', 'Plain text: invalid YAML',
        ):
            with self.subTest(description=description):
                source.write_text(
                    f"---\nname: new-source\ndescription: {description}\n---\n## When to use\nUse it for work.\n",
                    encoding="utf-8",
                )
                with self.assertRaises(publisher.FeedError):
                    publisher.publish_feed(self.root, date(2026, 9, 13), write=True, today=date(2026, 9, 13))
                self.assertEqual(before, (self.root / "skills.json").read_bytes())

    def test_quoted_descriptions_are_decoded_without_losing_content(self) -> None:
        self.add_skill("new-source")
        source = self.root / "skills" / "new-source" / "SKILL.md"
        for encoded, expected in (
            ('"Use \\"quotes\\" and \\\\paths; \\u0061 works."', 'Use "quotes" and \\paths; a works.'),
            ("'Use the author''s examples.'", "Use the author's examples."),
            ('"null"', 'null'),
            ('"Keep # text" # metadata comment', 'Keep # text'),
            ('Use plain text. # metadata comment', 'Use plain text.'),
        ):
            with self.subTest(encoded=encoded):
                source.write_text(
                    f"---\nname: new-source\ndescription: {encoded}\n---\n## When to use\nUse it for work.\n",
                    encoding="utf-8",
                )
                output, _ = publisher.publish_feed(self.root, date(2026, 9, 13), today=date(2026, 9, 13))
                self.assertEqual(output["weeks"][0]["skills"][0]["description"], expected)

    def test_duplicate_frontmatter_keys_are_rejected(self) -> None:
        self.add_skill("new-source")
        source = self.root / "skills" / "new-source" / "SKILL.md"
        source.write_text(source.read_text().replace("---\n\n##", "description: Duplicate.\n---\n\n##"))
        with self.assertRaisesRegex(publisher.FeedError, "duplicate frontmatter key"):
            publisher.publish_feed(self.root, date(2026, 9, 13), today=date(2026, 9, 13))

    def test_mapping_separator_requires_whitespace(self) -> None:
        self.add_skill("new-source")
        source = self.root / "skills" / "new-source" / "SKILL.md"
        source.write_text(source.read_text().replace("name: new-source", "name:new-source"))
        with self.assertRaisesRegex(publisher.FeedError, "malformed frontmatter line"):
            publisher.publish_feed(self.root, date(2026, 9, 13), today=date(2026, 9, 13))


if __name__ == "__main__":
    unittest.main()
