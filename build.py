import json,re
d=json.load(open('../discovery/sewing-data.json'))
def num(x):
    if x is None: return None
    s=str(x).strip().replace('"','')
    m=re.match(r'^(\d+)?\s*(\d+)/(\d+)$',s)
    if m: return float(m.group(1) or 0)+int(m.group(2))/int(m.group(3))
    return float(s)
def rng(v):
    if isinstance(v,dict): return [num(v['min']),num(v['max'])]
    return None if v is None else [num(v),num(v)]
# draft diff (cm), bust rule per range label; sources
META={
 'B cup 0-20':dict(diff=5.08,note='Drafted for a B cup'),
 'D cup 14-32':dict(diff=10.16,note='Drafted for a D cup, pear-shaped lower body'),
 'Alpha 2023 XXS-4X (A-D cup)':dict(diff=None,note='Page says it covers A-D cups'),
 'Alpha 2024+ XXS-6X':dict(diff=None,note='Same measurements as the 2023 chart, more sizes'),
 'XS-7X (first table, no header label; inch marks)':dict(diff=5.08,note='Drafted for a B cup',cm=False),
 "Women's 4-26 (XS-XXL)":dict(diff=2.54,note="Women's: drafted for a C cup, 1 in between bust and high bust"),
 "Women's Plus 16W-38W (1X-6X), second table under Women's heading":dict(diff=None,note='Plus table; the page does not state the cup',hb=True),
 'Sizes 12-32':dict(diff=None,note='Cup sizes C-H; sized by high bust',hb=True),
 'Sizes 0-16':dict(diff=None,note='Cup sizes C-H; sized by high bust',hb=True),
}
out=[]
for b in d['brands']:
    rs={}
    for r in b['ranges']:
        if r['unit']!='cm': continue
        lab=r['label']
        m=dict(META.get(lab,{}))
        if b['brand']=='Friday Pattern Co': m=dict(diff=5.08,note='Drafted for a B cup')
        if b['brand']=='Style Arc': m=dict(diff=5.08,note='Drafted for a B cup, Australian sizes')
        sizes=[]
        for s in r['sizes']:
            bu=s.get('bust') or (s.get('bust_by_cup') or {}).get('C/D')
            sizes.append(dict(size=str(s['size']).upper() if b['brand']=='Friday Pattern Co' else str(s['size']),
                bust=rng(bu),hb=rng(s.get('high_bust')),waist=rng(s.get('waist')),hip=rng(s.get('hip'))))
        out.append(dict(brand=b['brand'],range=lab.replace(', second table under Women\'s heading','').replace(', cm','').replace(' (table headed "CM")','').replace(', inches',''),
            url=b['source_url'],checked=b['date_checked'],diff=m.get('diff'),note=m.get('note',''),hb=m.get('hb',False),sizes=sizes))
out+=json.load(open('extra.json'))
json.dump(out,open('sizes.json','w'),indent=0)
html=open('template.html').read().replace('/*DATA*/',json.dumps(out))
open('index.html','w').write(html)
print(len(out),[ (o['brand'],o['range'],len(o['sizes'])) for o in out])
