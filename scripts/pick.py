#!/usr/bin/env python3
"""Pick countries to research this week -> /tmp/pick.json"""
import json,os,datetime
T=datetime.date.today();v={r['country']:r for r in json.load(open('data/visa.json'))['records']}
news=json.load(open('/tmp/news.json')) if os.path.exists('/tmp/news.json') else []
chk=json.load(open('/tmp/check.json')) if os.path.exists('/tmp/check.json') else {'deadLinks':[]}
import subprocess
subprocess.run(['python3','scripts/fetch_suggestions.py'],capture_output=True)
try:sg=json.load(open('/tmp/suggestions.json'))
except Exception:sg=[]
pick=[];why={}
def add(c,w):
    if c in v and c not in pick and len(pick)<12:pick.append(c);why[c]=w
for x in sg:add(x['country'],'reader suggestion: '+x.get('section','')+' | '+x.get('what','')[:80])
for h in news:add(h['country'],'news: '+h['title'])
for d in chk['deadLinks']:
    for c in d['countries']:add(c,'source unreachable')
for c,r in sorted(v.items(),key=lambda x:x[1]['lastChecked']):add(c,'oldest check '+r['lastChecked'])
json.dump({'also_check':['apply','health','transit'],'countries':pick,'why':why},open('/tmp/pick.json','w'),indent=1,ensure_ascii=False);print(json.dumps(why,indent=1,ensure_ascii=False))
