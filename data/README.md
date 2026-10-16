# Data files

Every record carries `lastChecked` (ISO date) and `sources` (links). The site reads these files at load time, so updating a file updates the site with no code change.

- `visa.json`: one record per country for an Indian ordinary passport. Fields: `country`, `trip`, `category` (visa_free, on_arrival, evisa, conditional, visa_required, unknown), `rule`, `easedBy` (US, SC, UK, CA, OT: which visas a traveller may hold that ease entry), `status` (confirmed, probable, uncertain), `sources`, `lastChecked`.
- `trips.json`: 18 trips (101 countries) with days, budget range in lakh of rupees, best months, countries, coordinates, tags.
- `experiences.json`: adventures, wildlife, stays and similar, with approximate rupee prices.
- `records.json`: record and bucket-list claims.

Rules for editing: never delete `lastChecked` or `sources`; change `status` to `uncertain` when sources disagree; keep prices as estimates; no personal data of any kind.

Known gaps (16 Oct 2026): many visa records cite Wikipedia's "Visa requirements for Indian citizens" or one official page, and `trips.json`, `experiences.json` and `records.json` have empty `sources` lists that still need links.
