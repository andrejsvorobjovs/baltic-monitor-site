# Continuity — how to keep this running without me

Baltic Signal Monitor is built and run by one person. If that person
stops — illness, war, death, or simply walking away — nothing here
restarts itself. The scans keep running on GitHub's schedule until an
API key expires or a bill goes unpaid, and then the site quietly goes
still while continuing to look normal.

This document exists so that "quietly goes still" is not the end of it.
It is written for a stranger: someone technical who wants to keep this
alive and has none of the context. **It lives in the public site
repository on purpose** — a handover note inside a private repo helps
nobody.

Nothing secret is in this file. It names which credentials exist and
what each is for; it never contains a value.

---

## First: is it actually dead?

The site says so itself. After **10 days** with no completed scan, a
banner appears on every page stating plainly that the operator may no
longer be able to run it. That check runs in the visitor's own browser
against the timestamp in `status.json`, so it still works when the
backend is entirely gone — a stopped server cannot report that it
stopped.

Before assuming the worst, check:

1. `https://balticsignalmonitor.com/status.json` → `last_run_utc`
2. The Actions tab of the private engine repo, if you have access
3. GitHub Actions billing — the most common non-fatal cause is a spent
   free-minutes budget, not a broken pipeline

A gap of a few days is normal-ish; GitHub's scheduler drifts and free
minutes run out. Ten days is not.

---

## What the thing is made of

Three repositories, three jobs.

| Repository | Visibility | What it does |
|---|---|---|
| `baltic-monitor` | **private** | The engine. All scanning, scoring, alerting. One large Python file plus tests, driven by GitHub Actions. |
| `baltic-monitor-site` | public | This repo. The website, served by GitHub Pages at balticsignalmonitor.com. The engine commits its published state into it. |
| `baltic-monitor-push` | public | A small serverless backend on Vercel that stores browser push subscriptions and delivers notifications. |

**Why the engine is private, and why that matters to you.** It contains
the keyword and source lists that decide what counts as a signal.
Published, they become a specification for how to feed the detector or
slip past it. That is a deliberate trade against openness, and it is the
single biggest obstacle to anyone continuing this work: *you cannot
take this over without access to that repository.* See "If you cannot
get access" below.

### The engine, in one paragraph

Roughly every four hours a scheduled workflow fetches ~150 sources —
some read directly from the publishing organisation, some through search
aggregation, plus non-news feeds (aviation notices, vessel positions,
GPS interference reports, grid data, thermal hotspots). Each item is
matched against keyword categories, filtered for relevance, grouped into
stories, and scored. One relevant item produces **WATCH**. Several
independent sources converging on the same story produce **WARN**.
Everything else is **QUIET**. The result is written to state files,
committed to this repo as `status.json` and friends, and pushed to
subscribers.

### Where the state lives

There is no database. Every piece of durable state is a JSON file
committed into the private repo — scan history, alert judgements,
corrections, per-source yield, escalation index history. This is
deliberate: it means the entire operating record is in git history, and
a clone is a complete backup. It also means two workflows writing at
once will conflict, which is why they share a concurrency group.

### Scheduled work

`scan.yml` is the heartbeat. `health-check.yml` runs twice daily as a
cheap freshness watchdog. `trend.yml` and `weekly_summary.yml` run
Mondays. The digests and `correction.yml` are triggered by hand. If you
inherit this and want to reduce cost, the scan cadence is the only dial
that matters — it dominates the Actions minutes bill.

### Delivery channels

Telegram channel, Mastodon, Bluesky, Discord, browser push, RSS, and the
website itself. Losing any one of them is survivable; the website and
RSS need no credentials at all and will outlive the rest.

---

## Credentials you would need

Names only. Every one is stored as a GitHub Actions secret on the engine
repo, except the push backend's, which live in Vercel's environment
settings.

**Cannot operate without these:**

- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`, `TELEGRAM_CHAT_ID` —
  the public channel and the owner's private control chat
- `PAGES_REPO_TOKEN` — lets the engine commit into this site repo

**Feature-specific; the scan degrades gracefully without each:**

- `MASTODON_ACCESS_TOKEN`, `MASTODON_INSTANCE_URL`
- `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD`
- `DISCORD_WEBHOOK_URL`
- `WEB_PUSH_NOTIFY_SECRET` — must match the value in the push backend
- `AISSTREAM_API_KEY` (vessel positions), `ENTSOE_API_KEY` (grid),
  `FIRMS_MAP_KEY` (thermal hotspots), `GDELT_CLOUD_API_KEY`
- `HEALTHCHECKS_PING_URL` — external dead-man's ping

Also outside GitHub: the **domain registration** for
balticsignalmonitor.com, the **Vercel** project, and its **Upstash
Redis** store.

---

## If you cannot get access

You probably cannot get the private repo, the domain, or the
credentials. Assume that, and read this section first rather than last.

What is genuinely yours to take, today, with no permission from anyone:

- **This repository.** Public. Contains the entire website, every
  language, the full method description, and the brand assets with their
  vector sources. Fork it.
- **The published record.** `status.json`, `chart_data.json`,
  `history_export.csv`, `escalation_export.csv`, `feed.xml`, and the
  corrections log are all public files in this repo, with full git
  history. That is the complete outcome record of every scan — you can
  audit the whole track record without any private access.
- **The method.** The site documents the tiering, the corroboration
  rule, and the escalation index in enough detail to rebuild an
  equivalent engine. The keyword lists are the part you would have to
  write yourself, and honestly, writing your own is better than
  inheriting mine.

**Do not** register a lookalike domain and continue under this name.
Whatever you build, build it under your own name. A warning channel that
changes hands invisibly is exactly the failure this whole project is
supposed to argue against — and the corrections log, the precision
figure, and the "not affiliated with any government" claim are all
promises made by a specific person. They are not transferable by
default.

---

## For whoever handles my affairs

If you are reading this because the person who ran it is gone, and you
have access to their accounts, the kindest order of operations is:

1. **Say so publicly.** Post once to the Telegram channel that the
   project is unmaintained. People are relying on this for warnings; the
   worst outcome is a channel that looks alive and is not.
2. **Do not delete anything.** The site costs nothing to leave up, and
   the public record has value even frozen. The 10-day banner will tell
   every visitor the truth by itself.
3. **Then decide slowly.** Handing the credentials to a stranger is not
   urgent and cannot be undone. Freezing it is reversible; transferring
   it is not.

Contact for anything here: **security@balticsignalmonitor.com**

---

## Known gaps in this plan

Stated rather than hidden, because a continuity plan that oversells
itself is worse than none:

- **No second person holds the credentials.** This is the real
  single point of failure and this document does not fix it. It only
  makes the aftermath survivable.
- **No legal entity owns anything.** Domain, accounts, and repositories
  sit with one individual, which makes an orderly transfer harder than
  it needs to be.
- **The keyword corpus has no succession path at all.** It is private,
  it is the hard-won part, and nobody else has a copy.
