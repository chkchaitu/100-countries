#!/usr/bin/env python3
"""Merge review11/bNN.json files into data/apply.json and test links. Usage: merge_apply.py b01 b02 ..."""
import json,re,sys,subprocess,concurrent.futures as cf
D='/home/azureuser/build/100-countries/review11/'
SCH={'France','Italy','Spain','Netherlands','Switzerland','Austria','Belgium','Portugal','Greece','Sweden','Norway','Denmark','Finland','Poland','Czechia','Hungary','Iceland','Germany','Estonia','Latvia','Lithuania','Luxembourg','Malta','Slovakia','Slovenia','Liechtenstein','Croatia'}
atlas={p['country'] for p in json.load(open('data/countries.json'))}
ap={a['country']:a for a in json.load(open('data/apply.json'))}
def clean(s):
    if isinstance(s,str):return re.sub(r'\s{2,}',' ',s.replace('\u2014',', ').replace('\u2013','-').replace('\u2019',"'"))
    if isinstance(s,list):return [clean(x) for x in s]
    if isinstance(s,dict):return {k:clean(x) for k,x in s.items()}
    return s
new=[]
for b in sys.argv[1:]:
    for x in clean(json.load(open(D+b+'.json',encoding='utf-8'))):
        assert x['country'] in atlas,x['country']
        new.append(x)
def chk(u):
    try:
        r=subprocess.run(['curl','-sIL','-m','20','-A','Mozilla/5.0','-o','/dev/null','-w','%{http_code}',u],capture_output=True,text=True,timeout=30)
        return u,int(r.stdout.strip() or 0)
    except Exception:return u,0
urls=sorted({u['url'] for x in new for k in('applyLinks','formLinks') for u in x.get(k,[]) if str(u.get('url','')).startswith('http')})
with cf.ThreadPoolExecutor(8) as ex:res=dict(ex.map(chk,urls))
ok=bad=blocked=0;dropped=[]
for x in new:
    for k in('applyLinks','formLinks'):
        keep=[]
        for u in x.get(k,[]):
            s=res.get(u.get('url'),-1)
            if 200<=s<400:keep.append(u);ok+=1
            elif s in(403,429,401,405,999,503) and s!=0:keep.append(u);blocked+=1
            else:dropped.append((x['country'],u.get('url'),s));bad+=1
        x[k]=keep
    x['sources']=[u for u in x.get('sources',[]) if str(u).startswith('http')]
    if x['country'] in SCH:x['schengenNote']="Applies the Schengen short-stay rules; apply through this country's own mission or visa centre."
    if not x.get('applyLinks') and not x.get('formLinks'):x.setdefault('unverified',[]).append('No working official apply link could be confirmed. Search for the official visa page.')
    ap[x['country']]=x
json.dump(list(ap.values()),open('data/apply.json','w'),indent=1,ensure_ascii=False)
print('merged',len(new),'total',len(ap),'| links ok',ok,'blocked-kept',blocked,'dropped',bad)
for d in dropped:print(' DROPPED',d)
print('no links:',[x['country'] for x in new if not x['applyLinks'] and not x['formLinks']])
import collections;print(collections.Counter(x['confidence'] for x in new))
