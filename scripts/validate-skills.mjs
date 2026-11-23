#!/usr/bin/env node
// Contract check for this repository.
//
// skills-log has no code: it is a skills index (skills.json) plus one directory
// per skill under skills/. That makes it easy for a repository like this to
// drift silently -- a skill is added and never indexed, a SKILL.md is renamed
// but the index still says the old name, or an entry points at a directory that
// no longer exists. None of that breaks a build, because there is no build.
//
// This script enforces the invariant the README already documents:
//   "skills.json lists every skill from every week"
// and the frontmatter contract every SKILL.md already follows.
//
// It is deliberately dependency-free so it can run anywhere.
//
// Exit 0 = the index and the tree agree. Exit 1 = they do not, with a reason.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const INDEX = join(ROOT, "skills.json");
const SKILLS_DIR = join(ROOT, "skills");

const failures = [];
const fail = (where, why) => failures.push(`${where}: ${why}`);
const nonEmpty = (v) => typeof v === "string" && v.trim() !== "";

// ---------------------------------------------------------------- index file
let index;
try {
  index = JSON.parse(readFileSync(INDEX, "utf8"));
} catch (err) {
  console.error(`FAIL skills.json could not be parsed: ${err.message}`);
  process.exit(1);
}

if (!nonEmpty(index.updated)) fail("skills.json", "missing non-empty `updated`");
if (!Array.isArray(index.weeks) || index.weeks.length === 0) {
  fail("skills.json", "`weeks` must be a non-empty array");
}

const weeks = Array.isArray(index.weeks) ? index.weeks : [];
const entries = [];
const seenSlugs = new Map();

for (const [wi, week] of weeks.entries()) {
  const label = `weeks[${wi}]`;
  if (!nonEmpty(week.week)) fail(label, "missing non-empty `week`");
  if (!nonEmpty(week.date)) fail(label, "missing non-empty `date`");
  if (!Array.isArray(week.skills) || week.skills.length === 0) {
    fail(label, "`skills` must be a non-empty array");
    continue;
  }

  for (const [si, skill] of week.skills.entries()) {
    const where = `${label}.skills[${si}]${nonEmpty(skill?.slug) ? ` (${skill.slug})` : ""}`;

    for (const field of ["name", "slug", "description", "useFor", "path"]) {
      if (!nonEmpty(skill?.[field])) fail(where, `missing non-empty \`${field}\``);
    }
    if (!nonEmpty(skill?.slug) || !nonEmpty(skill?.path)) continue;

    // The index points at a directory; it must equal skills/<slug>. A path that
    // disagrees with the slug is an entry nobody can resolve reliably.
    if (skill.path !== `skills/${skill.slug}`) {
      fail(where, `path "${skill.path}" must be "skills/${skill.slug}"`);
    }

    // A slug identifies one skill. Two weeks may list the same skill only if
    // they are pointing at the same record; duplicate slugs make every lookup
    // ambiguous.
    if (seenSlugs.has(skill.slug)) {
      fail(where, `duplicate slug "${skill.slug}" (already at ${seenSlugs.get(skill.slug)})`);
    } else {
      seenSlugs.set(skill.slug, where);
    }

    entries.push({ ...skill, where });
  }
}

// ------------------------------------------------------------- tree ↔ index
// 1. Every indexed path must exist and carry a SKILL.md with valid frontmatter.
for (const entry of entries) {
  const dir = join(ROOT, entry.path);
  if (!existsSync(dir) || !statSync(dir).isDirectory()) {
    fail(entry.where, `path "${entry.path}" is not a directory on disk`);
    continue;
  }

  const skillMd = join(dir, "SKILL.md");
  if (!existsSync(skillMd)) {
    fail(entry.where, `missing ${entry.path}/SKILL.md`);
    continue;
  }

  const text = readFileSync(skillMd, "utf8");
  const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!fm) {
    fail(`${entry.path}/SKILL.md`, "missing YAML frontmatter block");
    continue;
  }

  const front = fm[1];
  const read = (key) => {
    const m = new RegExp(`^${key}:[ \\t]*(.+)$`, "m").exec(front);
    return m ? m[1].trim() : null;
  };

  const fName = read("name");
  const fDesc = read("description");
  if (!nonEmpty(fName)) fail(`${entry.path}/SKILL.md`, "frontmatter missing non-empty `name:`");
  if (!nonEmpty(fDesc)) fail(`${entry.path}/SKILL.md`, "frontmatter missing non-empty `description:`");

  // The index and the file must agree. This is the check that catches a rename
  // in one place and not the other -- the failure a human reviewer misses.
  if (nonEmpty(fName) && fName !== entry.name) {
    fail(entry.where, `index name "${entry.name}" != SKILL.md frontmatter name "${fName}"`);
  }
}

// 2. Every skill directory on disk must be indexed. An unindexed skill is
//    invisible to every consumer of skills.json, which is the whole point of
//    the repository.
if (existsSync(SKILLS_DIR)) {
  const onDisk = readdirSync(SKILLS_DIR).filter((name) =>
    statSync(join(SKILLS_DIR, name)).isDirectory()
  );
  const indexed = new Set(entries.map((e) => e.slug));
  for (const name of onDisk) {
    if (!indexed.has(name)) fail(`skills/${name}`, "directory exists but is not indexed in skills.json");
  }
  for (const slug of indexed) {
    if (!onDisk.includes(slug)) fail(`skills/${slug}`, "indexed in skills.json but no such directory");
  }
}

// ------------------------------------------------------------------- result
if (failures.length > 0) {
  console.error(`FAIL ${failures.length} contract violation(s):`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}

console.log(
  `VERIFIED skills index: ${entries.length} skills across ${weeks.length} weeks, ` +
    `every entry resolves to a SKILL.md whose frontmatter name matches, ` +
    `no unindexed skill directories.`
);
