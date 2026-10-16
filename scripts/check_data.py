#!/usr/bin/env python3
"""Validate data files, check source links, list stale records. Exit 1 only on schema errors."""
import json,sys,datetime,urllib.request,concurrent.futures as cf
TODAY=datetime.date.today()
L=lambda p:json.load(open(p,encoding='utf-8'))
trips,visa,prof=L('data/trips.json'),L('data/visa.json'),L('data/countries.json')
err,warn=[],[]
atlas={c for t in trips['trips'] for c in t['countries']}|set(trips.get('hubs',{}).get('countries',[]))|set(trips.get('extras',{}).get('countries',[]))
vr={r['country']:r for r in visa['records']};pr={p['country']:p for p in prof}
for c in sorted(atlas):
    if c not in vr:err.append(f'{c}: no visa record')
    if c not in pr:err.append(f'{c}: no profile')
for c in sorted((set(vr)|set(pr))-atlas):err.append(f'{c}: in data but not in any trip or hub')
CATS={'visa_free','on_arrival','evisa','conditional','visa_required','unknown'}
for c,r in vr.items():
    if r.get('category') not in CATS:err.append(f'{c}: bad category {r.get("category")}')
    for k in('rule','status','sources','lastChecked'):
        if not r.get(k):err.append(f'{c}: visa missing {k}')
    try:datetime.date.fromisoformat(r['lastChecked'])
    except Exception:err.append(f'{c}: bad lastChecked')
    for k in r.get('easedBy',[]):
        if k not in visa['visaKeys']:err.append(f'{c}: unknown easedBy {k}')
for c,p in pr.items():
    for k in('region','places','bestMonths','sources','lastChecked'):
        if not p.get(k):err.append(f'{c}: profile missing {k}')
    if any(not(1<=m<=12) for m in p.get('bestMonths',[])):err.append(f'{c}: bad month')

# apply.json (how to apply): pilot covers some countries only
import os,re as _re
if os.path.exists('data/apply.json'):
    ap=L('data/apply.json')
    for a in ap:
        c=a.get('country')
        if c not in pr:err.append(f'apply: {c} not in countries.json')
        if not a.get('lastChecked'):err.append(f'apply: {c} missing lastChecked')
        if a.get('confidence') not in('official','partial','thin'):err.append(f'apply: {c} bad confidence')
        for k in('applyLinks','formLinks'):
            for u in a.get(k,[]):
                if not str(u.get('url','')).startswith('http'):err.append(f'apply: {c} bad url in {k}')
        if _re.search('[\u2014\u2013]',json.dumps(a,ensure_ascii=False)):err.append(f'apply: {c} has em or en dash')
# stale (visa rules go stale after 45 days, profiles after 180)
stale=[]
for c,r in vr.items():
    age=(TODAY-datetime.date.fromisoformat(r['lastChecked'])).days
    if age>45:stale.append((age,c,'visa'))
for c,p in pr.items():
    age=(TODAY-datetime.date.fromisoformat(p['lastChecked'])).days
    if age>180:stale.append((age,c,'profile'))
stale.sort(reverse=True)
# links
urls={}
for c,r in vr.items():
    for u in r['sources']:urls.setdefault(u,[]).append(c)
for c,p in pr.items():
    for u in p['sources']:urls.setdefault(u,[]).append(c)
def chk(u):
    for m in('HEAD','GET'):
        try:
            rq=urllib.request.Request(u,method=m,headers={'User-Agent':'Mozilla/5.0 (data-check)'})
            return u,urllib.request.urlopen(rq,timeout=20).status
        except urllib.error.HTTPError as e:
            if e.code in(403,405,429,999) :return u,-e.code   # blocked bots, not proof of a dead link
            last=e.code
        except Exception as e:last=str(e)[:40]
    return u,last
dead=[]
if '--links' in sys.argv:
    with cf.ThreadPoolExecutor(8) as ex:
        for u,s in ex.map(chk,urls):
            if not(isinstance(s,int) and (200<=s<400 or s<0)):dead.append((u,s,urls[u]))
out={'date':str(TODAY),'errors':err,'stale':[{'country':c,'kind':k,'ageDays':a} for a,c,k in stale],'deadLinks':[{'url':u,'status':s,'countries':cs} for u,s,cs in dead],'urlsChecked':len(urls) if '--links' in sys.argv else 0}
json.dump(out,open('/tmp/check.json','w'),indent=1)
print(f'errors {len(err)} | stale {len(stale)} | dead links {len(dead)} | urls {out["urlsChecked"]}')
for e in err[:30]:print(' ERR',e)
sys.exit(1 if err else 0)
