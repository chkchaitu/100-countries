# Weekly research playbook (visa and arrival rules)

Repo: ~/build/100-countries-site (chkchaitu/100-countries). Audience: Indian ordinary passport holders. Never put personal data in the repo.

1. `cd ~/build/100-countries-site && git checkout main && git pull -q`
2. `python3 scripts/news_watch.py; python3 scripts/check_data.py --links; python3 scripts/pick.py` and read /tmp/pick.json (about 12 countries: news triggers first, then stalest visa records, then countries whose sources failed).
3. For each picked country, find the OFFICIAL source first (immigration authority, foreign ministry, embassy or consulate in India, official e-visa portal). News and aggregator sites are only leads. Check: visa category for Indians, stay length, fee, e-visa or arrival card or travel authorisation, passport validity, any date the rule ends or starts, and any rule that an Indian's US, UK, Schengen or other visa waives.
4. Change a record in data/visa.json only when an official or two independent reliable sources support it. Update `rule`, `category`, `easedBy`, `status` (confirmed / probable), `sources` (real URLs only), and set `lastChecked` to today. If a country's rule is unchanged, only bump `lastChecked` and add the source you used. If you cannot verify, leave the record unchanged and list it as "unverified". Never guess. Rules are plain English, no em dashes.
5. If a country's profile (data/countries.json) is affected (for example an arrival card, a fee), update that too.
6. Run `python3 scripts/check_data.py` (must pass). Branch `research/YYYY-MM-DD`, commit, push, `gh pr create` with a body listing for each country: old rule, new rule, source links, confidence.
7. Wait for the PR check ("Weekly data check") to pass, then `gh pr merge --squash --delete-branch`. If the check fails, fix it once; if still failing, leave the PR open and say so.
8. Close the current weekly data-check issue with a comment that links the PR.
9. Final reply (goes to WhatsApp): a short weekly summary. Sections: Changed (country, old to new, source link), Confirmed unchanged (count and names), Could not verify, News triggers that did not matter, Source links that are dead. Plain text, no tables, no em dashes.
