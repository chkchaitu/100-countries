#!/usr/bin/env python3
"""Scan Google News RSS for visa or entry news per country (last 8 days). Writes /tmp/news.json. Never fails the run."""
import json,re,time,html,urllib.request,urllib.parse,datetime
KEY=re.compile(r'visa|e-?visa|\beta\b|arrival card|entry (rule|requirement|fee)|visa[- ]free|on arrival|border|travel authori|immigration|permit',re.I)
prof=json.load(open('data/countries.json',encoding='utf-8'))
hits=[]
for p in prof:
    c=p['country'].replace('United States of America','United States')
    q=f'"{c}" visa Indian citizens OR Indians when:8d'
    u='https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-IN&gl=IN&ceid=IN:en'
    try:d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode('utf8','ignore')
    except Exception as e:print('feed error',c,e);time.sleep(2);continue
    for it in re.findall(r'<item>(.*?)</item>',d,re.S)[:6]:
        t=html.unescape(re.sub(r'<!\[CDATA\[|\]\]>','',(re.findall(r'<title>(.*?)</title>',it,re.S) or [''])[0])).strip()
        l=(re.findall(r'<link>(.*?)</link>',it,re.S) or [''])[0].strip()
        pd=(re.findall(r'<pubDate>(.*?)</pubDate>',it,re.S) or [''])[0]
        if KEY.search(t) and re.search(r'\bIndia|\bIndian',t) and c.lower().split()[0] in t.lower() and not re.search(r'work visa|study|student|y-axis|job',t,re.I):hits.append({'country':p['country'],'title':t,'link':l,'published':pd})
    time.sleep(0.6)
seen=set();uniq=[]
for h in hits:
    if h['title'] not in seen:seen.add(h['title']);uniq.append(h)
json.dump(uniq,open('/tmp/news.json','w'),indent=1,ensure_ascii=False)
print('news hits',len(uniq))
for h in uniq[:15]:print(' -',h['country'],'|',h['title'][:100])
