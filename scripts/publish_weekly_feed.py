#!/usr/bin/env python3
"""Publish a truthful weekly Skills Log batch from checked-in source files.

The publisher has no model, network, or secret dependency.  A source skill is
eligible only when it is a new ``skills/<slug>/SKILL.md`` directory with valid
frontmatter and a ``## When to use`` section.  If there is no eligible source,
the command fails instead of manufacturing a dated batch.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


MAX_BATCH_SIZE = 10
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING_RE = re.compile(r"(?m)^##\s+When to use\s*$")
NEXT_HEADING_RE = re.compile(r"(?m)^##\s+")


class FeedError(ValueError):
    """A source or feed invariant prevents a safe publication."""


def _frontmatter(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise FeedError(f"{path}: missing YAML frontmatter")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise FeedError(f"{path}: unterminated YAML frontmatter") from exc

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise FeedError(f"{path}: malformed frontmatter line")
        key = key.strip()
        if key in fields:
            raise FeedError(f"{path}: duplicate frontmatter key {key!r}")
        fields[key] = value.strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1 :])
    return fields, body


def _when_to_use(body: str) -> str | None:
    match = HEADING_RE.search(body)
    if not match:
        return None
    section = body[match.end() :]
    next_heading = NEXT_HEADING_RE.search(section)
    if next_heading:
        section = section[: next_heading.start()]
    for raw in section.splitlines():
        line = re.sub(r"^\s*[-*]\s+", "", raw).strip()
        if not line or line.startswith("```"):
            continue
        return re.sub(r"\s+", " ", line)
    return None


def _source_skill(path: Path, slug: str) -> dict[str, str]:
    fields, body = _frontmatter(path)
    if fields.get("name") != slug:
        raise FeedError(f"{path}: name must equal directory slug {slug!r}")
    description = fields.get("description", "").strip()
    if not description:
        raise FeedError(f"{path}: description is required")
    if not SLUG_RE.fullmatch(slug):
        raise FeedError(f"{path}: invalid directory slug")
    use_for = _when_to_use(body)
    if not use_for:
        raise FeedError(f"{path}: ## When to use must contain a non-empty paragraph")
    return {
        "name": fields["name"],
        "slug": slug,
        "description": description,
        "useFor": use_for,
        "path": f"skills/{slug}",
    }


def _validate_feed(feed: Any) -> tuple[list[dict[str, Any]], set[str]]:
    if not isinstance(feed, dict) or not isinstance(feed.get("weeks"), list):
        raise FeedError("skills.json must contain a weeks array")
    weeks = feed["weeks"]
    published: set[str] = set()
    for week in weeks:
        if not isinstance(week, dict) or not isinstance(week.get("skills"), list):
            raise FeedError("each feed week must contain a skills array")
        if not isinstance(week.get("week"), str) or not isinstance(week.get("date"), str):
            raise FeedError("each feed week must contain string week and date fields")
        try:
            dt.date.fromisoformat(week["date"])
        except ValueError as exc:
            raise FeedError(f"invalid existing week date {week['date']!r}") from exc
        for skill in week["skills"]:
            if not isinstance(skill, dict) or not isinstance(skill.get("slug"), str):
                raise FeedError("each feed skill must contain a string slug")
            slug = skill["slug"]
            if slug in published:
                raise FeedError(f"duplicate published skill {slug!r}")
            if skill.get("path") != f"skills/{slug}":
                raise FeedError(f"feed path mismatch for {slug!r}")
            published.add(slug)
    return weeks, published


def _week_id(publication_date: dt.date) -> str:
    # The historical feed labels a Sunday batch with the ISO week beginning
    # the following Monday (for example, 2026-09-06 is 2026-W37).
    iso = (publication_date + dt.timedelta(days=1)).isocalendar()
    return f"{iso.year:04d}-W{iso.week:02d}"


def _candidates(root: Path, published: set[str]) -> tuple[list[dict[str, str]], list[str]]:
    candidates: list[dict[str, str]] = []
    ineligible: list[str] = []
    skills_dir = root / "skills"
    for source_dir in sorted(skills_dir.iterdir()):
        if not source_dir.is_dir() or source_dir.name.startswith("."):
            continue
        source_path = source_dir / "SKILL.md"
        if not source_path.exists() or source_dir.name in published:
            continue
        try:
            candidates.append(_source_skill(source_path, source_dir.name))
        except FeedError as exc:
            ineligible.append(str(exc))
    return candidates, ineligible


def publish_feed(
    root: Path,
    publication_date: dt.date,
    *,
    write: bool = False,
    limit: int = MAX_BATCH_SIZE,
    today: dt.date | None = None,
) -> tuple[dict[str, Any], list[str]]:
    if publication_date.weekday() != 6:
        raise FeedError("publication date must be a Sunday")
    today = today or dt.datetime.now(dt.timezone.utc).date()
    if publication_date > today:
        raise FeedError("publication date cannot be in the future")

    feed_path = root / "skills.json"
    try:
        feed = json.loads(feed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FeedError(f"cannot read {feed_path}") from exc
    weeks, published = _validate_feed(feed)
    week_id = _week_id(publication_date)
    candidates, ineligible = _candidates(root, published)
    if ineligible:
        raise FeedError("Unpublished source skills are ineligible: " + "; ".join(ineligible))
    matching_week = next((week for week in weeks if week.get("week") == week_id), None)
    if matching_week:
        if matching_week.get("date") == publication_date.isoformat() and not candidates:
            return feed, []
        raise FeedError(f"week {week_id} is already published")
    existing_dates = [dt.date.fromisoformat(week["date"]) for week in weeks]
    if existing_dates and publication_date <= max(existing_dates):
        raise FeedError("publication date must be newer than the latest feed date")
    if not candidates:
        raise FeedError("No unpublished eligible skills; refusing to fabricate a weekly batch.")
    if len(candidates) > limit:
        raise FeedError(f"{len(candidates)} unpublished skills exceed the batch limit of {limit}; curate first")

    new_week = {"week": week_id, "date": publication_date.isoformat(), "skills": candidates}
    output = {**feed, "updated": publication_date.isoformat(), "weeks": [new_week, *weeks]}
    if write:
        feed_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output, [skill["slug"] for skill in candidates]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--date", required=True, help="Sunday publication date in YYYY-MM-DD form")
    parser.add_argument("--write", action="store_true", help="write skills.json; otherwise perform a dry run")
    args = parser.parse_args(argv)
    try:
        publication_date = dt.date.fromisoformat(args.date)
        _, slugs = publish_feed(args.root, publication_date, write=args.write)
    except (FeedError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    mode = "published" if args.write else "would publish"
    print(f"{mode} {len(slugs)} source skill(s) for {args.date}: {', '.join(slugs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
