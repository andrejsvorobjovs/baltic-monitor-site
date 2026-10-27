# tools/

Generators for the Russian pages.

`ru/` is not hand-maintained. It is built from `lv/` — the Latvian pages are
the ones already written for a reader inside the region, and the Russian
audience overlaps with that reader almost exactly: Russian-speaking residents
of Latvia and Estonia, roughly a quarter of each country's population, who are
the single group most targeted by Russian-state disinformation and least
served by Latvian- or Estonian-only sources.

    python3 tools/ru_index.py       # ru/index.html      from lv/index.html
    python3 tools/ru_subpages.py    # ru/privacy, ru/funding

Both are idempotent, and both FAIL (non-zero exit, with the offending string
printed) when any phrase in their tables no longer matches the Latvian source.
That is the point: **when you edit a Latvian page, rerun these.** A failure
means a sentence changed on the Latvian side and its Russian counterpart is
now stale — add or update the pair rather than deleting it, or the Russian
page silently keeps the old wording.

Three details worth knowing before editing the tables:

* Pairs are applied **longest-first**. Several strings are substrings of
  longer ones (a heading repeated inside a caption); shortest-first would
  make the long one unmatchable and leave it untranslated.
* Matching is **whitespace-tolerant** and treats `"`, `„`, `“` and `”` as
  interchangeable, because the source file mixes them for the same role.
* The prose pass never runs inside `<script>`. JavaScript strings have their
  own table in `script_pairs.py`, several of them sentence fragments
  concatenated around a number, so they are translated with the join in mind.
  A partial hit inside JavaScript produces a half-Latvian, half-Russian
  sentence at runtime — worse than no translation, because nothing in the
  source looks wrong.
