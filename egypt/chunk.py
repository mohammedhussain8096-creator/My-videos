import re, json, sys, spoken
T=32
text=open('script.txt').read().strip()
paras=[p.strip() for p in text.split('\n\n') if p.strip()]
units=[]
for p in paras:
    sents=re.split(r'(?<=[.?!"])\s+(?=[A-Z"])',p)
    for si,s in enumerate(sents):
        parts=re.split(r'(?<=[,;:])\s+',s) if len(s.split())>14 else [s]
        for k,u in enumerate(parts):
            units.append((u, k==len(parts)-1, si==len(sents)-1 and k==len(parts)-1))
W=[spoken.stats(u[0])[1] for u in units]; N=len(units)
INF=1e18; best=[INF]*(N+1); prev=[-1]*(N+1); best[0]=0
for j in range(1,N+1):
    n=0
    for i in range(j-1,-1,-1):
        n+=W[i]
        if n>46: break
        if n<18 and j<N: continue
        sent_end,para_end=units[j-1][1],units[j-1][2]
        c=(n-T)**2 + (60*(24-n) if n<24 and j<N else 0) + (60*(n-40) if n>40 else 0) + (0 if sent_end else 25) - (6 if para_end else 0)
        if best[i]+c<best[j]: best[j]=best[i]+c; prev[j]=i
cuts=[];j=N
while j>0: cuts.append((prev[j],j)); j=prev[j]
cuts.reverse(); out=[]
for i,j in cuts:
    t=''
    for k in range(i,j):
        t+=units[k][0]+(' // ' if units[k][2] and k<j-1 else ' ')
    out.append(t.strip())
json.dump(out,open('chunks.json','w'),indent=0)
for i,s in enumerate(out,1): print(i,spoken.stats(s)[1],s)
print(sum(len(s.replace('//','').split()) for s in out),'words',len(out),'scenes',file=sys.stderr)
