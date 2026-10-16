# Review of reader suggestions (every 3 days)

Repo ~/build/100-countries-site. Reports come from the anonymous "Suggest an update" Google Form into a Google Sheet. Every report is a LEAD, never a fact. Never copy a reader's wording into the data. Never record or repeat any personal details a reader may have typed.

1. `cd ~/build/100-countries-site && git checkout main && git pull -q`
2. Read the sheet: `gog sheets get <SHEET_ID> 'A:H' -j` (SHEET_ID is in scripts/suggestions.conf). Rows after the last processed row (stored in scripts/suggestions.state, a line number) are new. If there are no new rows, reply NO_REPLY.
3. For each new row (country, section, what changed, source link, how they know, date):
   - Open the source link. It must be an official page (government, embassy, immigration, health ministry, airline or airport authority). A blog, forum or news article is only a lead: find the official page yourself.
   - Decide: CONFIRMED (an official page supports the change), PARTLY (official page found but different from the report), CANNOT VERIFY (no official page readable), or REJECT (spam, wrong country, not about travel rules, contains personal data).
   - For CONFIRMED or PARTLY: edit the right file (data/visa.json, data/apply.json, data/health.json, data/health-global.json, data/transit.json, data/countries.json), set lastChecked to today and put the official URL in sources. Plain English, no em dashes.
4. Keep a log in data/suggestions-log.json: one entry per processed row with date, country, section, verdict, official URL used. Never store the reader's text verbatim if it contains personal data. Do not store emails or names.
5. Update scripts/suggestions.state to the last row processed.
6. `python3 scripts/check_data.py` must pass. If any data changed, write /tmp/pr-body.md (per change: old value, new value, official source, which report led to it) and run `scripts/finish_pr.sh "Reader suggestions YYYY-MM-DD" /tmp/pr-body.md`. A change that tightens or loosens entry rules must use `--no-merge` so Krishna approves it.
7. Final WhatsApp reply (plain text, no tables, no em dashes): how many reports, how many confirmed and changed (country, what, source), how many could not be verified, how many rejected, PRs left for approval.
