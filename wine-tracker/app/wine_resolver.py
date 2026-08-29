import re, unicodedata
from difflib import SequenceMatcher

def normalize(v):
    v=unicodedata.normalize('NFKD',v or '')
    v=''.join(c for c in v if not unicodedata.combining(c)).lower()
    return ' '.join(re.sub(r'[^a-z0-9]+',' ',v).split())

def score(q,c):
    q,c=normalize(q),normalize(c)
    if not q or not c:return 0
    qt,ct=set(q.split()),set(c.split())
    seq=SequenceMatcher(None,q,c).ratio()
    overlap=len(qt&ct)/max(1,len(qt|ct))
    contain=len(qt&ct)/max(1,len(qt))
    return round(seq*.45+overlap*.30+contain*.25,4)

def resolve(query, rows, limit=5):
    out=[]
    for r in rows:
        d=dict(r); text=' '.join(str(d.get(k) or '') for k in ('name','year','region','grape'))
        s=score(query,text)
        if s>=.18: out.append({**{k:d.get(k) for k in ('id','name','year','region','grape','vivino_id')},'confidence':s,'source':'local_cellar'})
    out.sort(key=lambda x:x['confidence'],reverse=True); out=out[:limit]
    top=out[0]['confidence'] if out else 0
    return {'query':query,'status':'matched' if top>=.78 else 'confirm' if top>=.48 else 'unknown','confidence':top,'candidates':out}
