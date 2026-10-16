#!/usr/bin/env python3
"""Fetch NEW reader suggestions from the Google Form -> /tmp/suggestions.json. Never fails the run.
A response is new if its responseId is not in data/suggestions-log.json."""
import json,subprocess,os
ID=open('scripts/suggestions.form').read().strip()
QID={'0c279769':'country','3f2a6f0d':'section','4f7cc33d':'what','4b1fa925':'source','4da2b879':'how'}
try:log=json.load(open('data/suggestions-log.json'))
except Exception:log=[]
done={e.get('responseId') for e in log}
out=[]
try:
    r=subprocess.run(['gog','forms','responses','list',ID,'-j'],capture_output=True,text=True,timeout=60)
    d=json.loads(r.stdout)
    for x in d.get('responses') or []:
        rid=x.get('responseId')
        if rid in done:continue
        a={}
        for q,v in (x.get('answers') or {}).items():
            vals=[t.get('value') for t in (v.get('textAnswers') or {}).get('answers',[])]
            if q in QID:a[QID[q]]=' | '.join(vals)
        if a.get('country'):out.append({'responseId':rid,'submitted':x.get('lastSubmittedTime') or x.get('createTime'),**a})
except Exception as e:print('fetch error',e)
json.dump(out,open('/tmp/suggestions.json','w'),indent=1,ensure_ascii=False)
print(len(out),'new suggestions',[(o['country'],o.get('section')) for o in out])
