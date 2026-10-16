#!/usr/bin/env python3
"""Pick the 10 stalest countries across profile, apply and health data -> /tmp/refresh.json"""
import json
L=lambda p:json.load(open(p,encoding='utf-8'))
pr={p['country']:p['lastChecked'] for p in L('data/countries.json')}
ap={a['country']:a['lastChecked'] for a in L('data/apply.json')}
hl={h['country']:h['lastChecked'] for h in L('data/health.json')}
age={c:min(pr.get(c,'0'),ap.get(c,'9999'),hl.get(c,'9999')) for c in pr}
pick=sorted(age,key=lambda c:(age[c],c))[:10]
json.dump({'countries':pick,'oldest':{c:age[c] for c in pick},'needsApply':[c for c in pick if c in ap]},open('/tmp/refresh.json','w'),indent=1)
print(json.dumps({c:age[c] for c in pick},indent=1))
