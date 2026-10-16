#!/usr/bin/env python3
"""Merge /tmp/check.json and /tmp/news.json into a markdown report (report.md)."""
import json,os
c=json.load(open('/tmp/check.json'));n=json.load(open('/tmp/news.json')) if os.path.exists('/tmp/news.json') else []
o=[f"# Weekly data check, {c['date']}\n",f"- Schema errors: **{len(c['errors'])}**",f"- Stale records (visa over 45 days, profile over 180): **{len(c['stale'])}**",f"- Source links checked: {c['urlsChecked']}, unreachable: **{len(c['deadLinks'])}**",f"- News items that may signal a rule change: **{len(n)}**\n"]
if c['errors']:o+=['## Schema errors']+[f'- {e}' for e in c['errors']]+['']
if n:o+=['## News triggers (research these first)']+[f"- **{h['country']}**: [{h['title']}]({h['link']})" for h in n]+['']
if c['stale']:o+=['## Stalest records']+[f"- {s['country']} ({s['kind']}, {s['ageDays']} days)" for s in c['stale'][:25]]+['']
if c['deadLinks']:o+=['## Unreachable sources (may be bot blocking, confirm by hand)']+[f"- {d['url']} ({d['status']}) for {', '.join(sorted(set(d['countries'])))}" for d in c['deadLinks']]+['']
open('report.md','w').write('\n'.join(o));print('\n'.join(o)[:1500])
