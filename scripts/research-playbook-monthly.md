# Monthly pass: profiles, fees, places, best months

Repo ~/build/100-countries-site. Weekly job covers visa rules; this pass covers everything else, rotating through the countries so each gets reviewed about every 6 months (about 20 per month).
1. `git checkout main && git pull -q`. Pick the 20 countries with the oldest profile `lastChecked` in data/countries.json (use `python3 -c` to list them).
2. Spawn research subagents (isolated, 4 countries each, at most 5 at a time). Each checks, for its countries: arrival or entry fees, tourist-attraction fees and opening status, seasonal closures, best months for low budget, transport links, safety or health advisories (official source such as the Indian MEA advisory or the country's tourism board), and any record or experience that is gone. Official or tourism-board sources first. Items not confirmable stay marked UNVERIFIED, never guessed.
3. Update data/countries.json (and records.json or experiences.json when affected); set `lastChecked` to today; fix `sources`. Plain English, no em dashes, no personal data.
4. `python3 scripts/check_data.py` must pass. Branch `research/monthly-YYYY-MM`, PR with old and new values and source links per country, wait for the check, `gh pr merge --squash --delete-branch`.
5. Every third month (January, April, July, October) also list countries whose visa `lastChecked` is over 90 days old and hand them to the weekly pick by listing them in the PR body.
6. Final reply to WhatsApp: changed (country, what, source), unchanged count, could not verify, dead links. Plain text, no tables, no em dashes.
