#!/usr/bin/env python3
"""Pick the 10 stalest countries across profile, apply and health data -> /tmp/refresh.json"""
import json
L=lambda p:json.load(open(p,encoding='utf-8'))
pr={p['country']:p['lastChecked'] for p in L('data/countries.json')}
ap={a['country']:a['lastChecked'] for a in L('data/apply.json')}
hl={h['country']:h['lastChecked'] for h in L('data/health.json')}
tx={h['country']:h['lastChecked'] for h in L('data/transit.json')}
age={c:min(pr.get(c,'0'),ap.get(c,'9999'),hl.get(c,'9999'),tx.get(c,'9999')) for c in pr}
import subprocess,os
subprocess.run(['python3','scripts/fetch_suggestions.py'],capture_output=True)
try:sg=json.load(open('/tmp/suggestions.json'))
except Exception:sg=[]
sc=[]
for x in sg:
    if x['country'] in age and x['country'] not in sc:sc.append(x['country'])
rest=[c for c in sorted(age,key=lambda c:(age[c],c)) if c not in sc]
pick=(sc+rest)[:max(10,len(sc))]
json.dump({'countries':pick,'oldest':{c:age[c] for c in pick},'suggestionCountries':sc,'needsApply':[c for c in pick if c in ap]},open('/tmp/refresh.json','w'),indent=1)
print(json.dumps({c:age[c] for c in pick},indent=1))
