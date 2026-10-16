# Refresh pass: profiles, how to apply, health, currency

Repo ~/build/100-countries-site. The weekly job covers visa rules and the daily job covers news. This pass reviews everything else for a rotating set of countries, so each country is rechecked about every 10 months (10 countries per run, runs on the 1st and 15th).
Do all research YOURSELF in this one turn, one country after another. Do NOT spawn subagents: a scheduled run cannot wait for them and ends early.

1. `cd ~/build/100-countries-site && git checkout main && git pull -q`
2. `python3 scripts/pick_refresh.py` and read /tmp/refresh.json (the 10 countries whose oldest `lastChecked` across countries.json, apply.json and health.json is the stalest).
3. For each picked country, check against OFFICIAL sources first (government, embassy, tourism board, WHO, CDC):
   - Profile (data/countries.json): entry or attraction fees and opening status, seasonal closures, best months for low budget, transport, safety advisories (India's MEA advisory, tourism board), gone experiences. Currency name, code and symbol still correct.
   - How to apply (data/apply.json, only if the country needs a visa): apply links still open (curl -sIL -m 20), forms, documents, photo spec, fee, processing time, centres, whether the route changed (for example a new e-visa portal or a suspended service). Drop dead links, add the new official link.
   - Health (data/health.json): yellow fever entry rule from India, required and recommended vaccines, malaria, new health notices (CDC, WHO, the destination health ministry). If a country is added to or removed from India's yellow fever or polio lists, update data/health-global.json.
   Items you cannot confirm stay UNVERIFIED. Never guess. Plain English, no em dashes, no personal data.
4. Update the files, set `lastChecked` to today for every country you really checked, fix `sources` and `confidence`. If you could not check a country properly, leave its `lastChecked` unchanged and list it as "not done".
5. Write the PR body to /tmp/pr-body.md (per country: what changed, old and new value, source links). Run `python3 scripts/check_data.py` (must pass), then `scripts/finish_pr.sh "Refresh pass YYYY-MM-DD" /tmp/pr-body.md`. It branches, opens the PR, waits for the check and merges. If there are no changes, do not run it.
6. Never end the turn waiting for anything. The run counts as a success only if finish_pr.sh printed MERGED, or you honestly found nothing to change after really checking every picked country.
7. Final reply to WhatsApp (plain text, no tables, no em dashes): changed (country, what, source link), confirmed unchanged (count and names), could not verify, dead links removed, countries not done.
