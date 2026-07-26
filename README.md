# Baltic Signal Monitor — Public Site

This repo holds only the public landing page for Baltic Signal Monitor —
an independent, free early-warning channel tracking Baltic/Russia
security signals.

It's deliberately separate from the main project's repo, which stays
private (it contains the full source list and scoring logic). This repo
contains nothing but the static page and a small `status.json` data file
that the main project's health-check workflow updates automatically.

- `index.html` — the page itself
- `status.json` — live track-record data, overwritten automatically on
  every health check (no need to edit this by hand)

Served via GitHub Pages, pointed at `balticsignalmonitor.com`.
