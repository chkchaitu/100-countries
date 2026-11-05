---
name: Atlas verify pilot
description: Pilot. Re-verify the 4 stalest countries against official sources and open a draft PR with data changes only.
on:
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
engine: copilot
strict: true
timeout-minutes: 45
network:
  allowed:
    - defaults
    - github
    - python
    - "*.gov"
    - "*.gov.in"
    - "*.gov.uk"
    - "*.europa.eu"
    - "*.int"
    - "*.org"
tools:
  github:
    mode: gh-proxy
    toolsets: [default]
  edit:
  bash: ["python3", "git", "curl", "cat", "grep", "ls", "head", "tail", "sed", "jq"]
safe-outputs:
  create-pull-request:
    title-prefix: "[gh-aw pilot] "
    labels: [automation, pilot]
    draft: true
    max: 1
    if-no-changes: ignore
    allowed-files:
      - "data/*.json"
    protected-files: fallback-to-issue
  noop:
---

# Atlas verify pilot

You maintain the world atlas in this repo (world.chaitu.in). Audience: Indian ordinary passport holders. Plain English, no em or en dashes, no personal data.

## Task

1. Read `scripts/research-playbook.md` and `scripts/research-playbook-monthly.md` for the rules, especially the UNVERIFIED rule. Do not run `finish_pr.sh` or push anything yourself; the safe output creates the pull request.
2. Pick exactly 4 countries: the ones with the oldest `lastChecked` across `data/visa.json`, `data/countries.json`, `data/apply.json`, `data/health.json` and `data/transit.json`. Use python to compute it; do not guess.
3. For each country, check against OFFICIAL sources first (government, embassy, immigration, tourism board, WHO, CDC, MEA or Indian embassy): the visa rule for Indian ordinary passports, profile fees and status, apply routes and official links, health entry rules, transit rules. Embassy fee pages often list other nationalities, so use the Indian row only. A news item or an aggregator is a lead, never a source.
4. Change a record only when an official page you actually read supports it. Update `lastChecked` only on sections you really re-read. If you cannot read a page (blocked, JavaScript only, outside the network allowlist), leave the record unchanged and list it as unverified. Never guess. Keep JSON indent, `ensure_ascii=False` style and a trailing newline.
5. Open one draft pull request. In the body, per country: old value, new value, official URL, confidence. Then a section "Not merged / unverified" with the reason for each (including any site the network firewall blocked), and a line saying how many of the 4 countries you could verify fully.
6. If you changed nothing, call `noop` with a short summary of what you checked.

Only files `data/*.json` may change.
