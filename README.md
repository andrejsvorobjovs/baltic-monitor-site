# Baltic Signal Monitor — Public Site

This repo holds only the public landing page for Baltic Signal Monitor —
an independent, free early-warning channel tracking Baltic/Russia
security signals.

It's deliberately separate from the main project's repo, which stays
private (it contains the full source list and scoring logic). This repo
contains nothing but the static page and a small `status.json` data file
that the main project's health-check workflow updates automatically.

- `index.html` — the page itself
- `status.json` — live track-record data, overwritten automatically by
  the main project on every scan/health check (no need to edit by hand)
- `chart_data.json` — longer time series behind the homepage's charts
  (escalation intensity, rumor/disinfo tracking, GPS-jamming, AIS vessel
  count, military aircraft count, NASA FIRMS thermal hotspots, and the
  Signal Deviation Index — an average of the other four's own
  deviation-from-baseline percentages, shown both as a prominent widget
  near the top of the page and as a full chart further down; a
  measurement, never a prediction, and never affects the WARN/WATCH/QUIET
  result), same auto-update mechanism
- `feed.xml` — RSS feed of recent flagged items, same auto-update mechanism
- `map/index.html` — a live map (Leaflet.js + OpenStreetMap tiles)
  plotting recent AIS ship, military ADS-B aircraft, GPS-jamming, and NASA
  FIRMS thermal-hotspot positions the main project already collects every
  scan — see its own prominent on-page caveat for the honesty limits
  (self-declared/spoofable data, snapshot not continuous tracking, never
  an alert on its own)
- `map_data.json` — the position data behind `map/index.html`, same
  auto-update mechanism as `status.json`/`chart_data.json`, overwritten by
  the main project's `main.py` at the end of every scan (no need to edit
  by hand; absent until the first scan after this feature shipped runs)
- `data/baltic-cables.geojson` — a static reference layer for `map/`: real
  submarine cable routes and landing points in the Baltic region, trimmed
  from TeleGeography's Submarine Cable Map
  (https://www.submarinecablemap.com/, © TeleGeography, CC BY-NC-SA 3.0)
  and bundled here rather than fetched live from a third party on every
  page load. Static — not part of the auto-update pipeline; re-fetch and
  re-trim by hand (see the file's own `properties` block for the source
  API and exact filtering used) if it ever needs refreshing.

Served via GitHub Pages, pointed at `balticsignalmonitor.com`.
