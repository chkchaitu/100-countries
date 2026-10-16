#!/usr/bin/env python3
"""Fast daily scan: broad Google News queries (not per country), keep items that mention an atlas country,
India or Indians, and a rule-change word. Dedupes with a state file outside the repo. Prints JSON."""
import json,re,html,os,sys,urllib.request,urllib.parse
ST=os.path.expanduser('~/build/100-countries/news-seen.json')
names=[p['country'] for p in json.load(open('data/countries.json',encoding='utf-8'))]
alias={'United States of America':'United States|USA|US ','United Arab Emirates':'UAE|Dubai|Abu Dhabi'}
pat={n:re.compile(r'\b(?:'+alias.get(n,re.escape(n))+r')\b',re.I) for n in names}
QS=['Indian citizens visa-free entry','Indian passport holders new visa rule','visa on arrival Indians','e-visa for Indian nationals','Indian travellers entry requirement change','visa fee hike Indian tourists','suspends visa Indians','arrival card Indian travellers']
CH=re.compile(r'visa[- ]free|free visa|e-?visa|visa on arrival|arrival card|visa fee|suspend|scrap|introduc|mandatory|new rule|ban|ends?|extend|waiv|resume|stop',re.I)
BAD=re.compile(r'work visa|student|study|PR\b|permanent|immigration pathway|green card|H-?1B|job|Y-Axis|golden',re.I)
seen=set(json.load(open(ST))) if os.path.exists(ST) else set()
new=[];keep=set(seen)
for q in QS:
    u='https://news.google.com/rss/search?q='+urllib.parse.quote(q+' when:2d')+'&hl=en-IN&gl=IN&ceid=IN:en'
    try:d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=10).read().decode('utf8','ignore')
    except Exception as e:continue
    for it in re.findall(r'<item>(.*?)</item>',d,re.S)[:12]:
        t=html.unescape(re.sub(r'<!\[CDATA\[|\]\]>','',(re.findall(r'<title>(.*?)</title>',it,re.S) or [''])[0])).strip()
        l=(re.findall(r'<link>(.*?)</link>',it,re.S) or [''])[0].strip()
        if t in keep or not re.search(r'\bIndia|\bIndian',t) or not CH.search(t) or BAD.search(t):continue
        c=[n for n in names if pat[n].search(t)]
        if not c:continue
        keep.add(t);new.append({'countries':c,'title':t,'link':l})
os.makedirs(os.path.dirname(ST),exist_ok=True)
if '--dry' not in sys.argv:json.dump(sorted(keep)[-2000:],open(ST,'w'))
print(json.dumps(new,ensure_ascii=False))
