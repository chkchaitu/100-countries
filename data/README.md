# Data files

Every record carries `lastChecked` (ISO date) and `sources` (links). The site reads these files at load time, so updating a file updates the site with no code change.

- `visa.json`: one record per country for an Indian ordinary passport. Fields: `country`, `trip`, `category` (visa_free, on_arrival, evisa, conditional, visa_required, unknown), `rule`, `easedBy` (US, SC, UK, CA, OT: which visas a traveller may hold that ease entry), `status` (confirmed, probable, uncertain), `sources`, `lastChecked`.
- `trips.json`: 34 trips (181 countries; the 16 trips with codes T to AJ are unresearched drafts) and a `hubs` group of 14 popular hub countries with days, budget range in lakh of rupees, best months, countries, coordinates, tags.
- `countries.json`: one profile per country (115): region, capital, places with fees, best months, daily budget in rupees, transport, experiences, cautions, neighbours, sources, lastChecked, confidence.
- `experiences.json`: adventures, wildlife, stays and similar, with approximate rupee prices.
- `records.json`: record and bucket-list claims.

Rules for editing: never delete `lastChecked` or `sources`; change `status` to `uncertain` when sources disagree; keep prices as estimates; no personal data of any kind.

Known gaps (16 Oct 2026): many visa records cite Wikipedia's "Visa requirements for Indian citizens" or one official page, and `trips.json`, `experiences.json` and `records.json` have empty `sources` lists that still need links.

- `apply.json`: how to apply for a visa from India, per country where a visa or pre-approval is needed: route, official apply and form links, documents checklist, photo spec, fee, processing, warnings, unverified items, confidence.
- `health.json`: per country entry vaccination rules for a traveller arriving directly from India (yellow fever entry rule, required and recommended vaccines, malaria, other notes), sources, confidence.
- `health-global.json`: rules for returning to India (yellow fever and polio lists, customs allowance, currency declaration), with the lists of yellow fever risk and polio advisory countries.
- `transit.json`: per country transit rules for Indian passport holders: airside (stay in the airport) and landside (leave the airport) visa needs, longest layover, transit schemes, which valid visas waive the transit visa, how to get a transit visa, fee, warnings, sources, confidence.
