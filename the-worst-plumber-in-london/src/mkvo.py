import wave,numpy as np,json,re
lines=[l.strip() for l in open('lines.txt') if l.strip()]
SR=22050; GAP=[0.22]*len(lines); START=0.2
for k,v in {0:0.35,3:0.3,6:0.4,9:0.4,12:0.3,13:0.35}.items(): GAP[k]=v
out=[np.zeros(int(START*SR))]; t=START; T=[]
for i,l in enumerate(lines):
    w=wave.open(f'vo/{i+1:02d}.wav'); assert w.getframerate()==SR
    a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-200):idx[-1]+1500]
    d=len(a)/SR
    words=l.split()
    env=np.convolve(np.abs(a),np.ones(441)/441,'same'); voiced=env>0.012
    sil=[];j=0;n=len(a)
    while j<n:
        if not voiced[j]:
            k=j
            while k<n and not voiced[k]: k+=1
            if (k-j)/SR>0.09 and j>0 and k<n: sil.append((j/SR,k/SR))
            j=k
        else: j+=1
    chunks=[[]]
    for wd in words:
        chunks[-1].append(wd)
        if re.search(r'[.,!?]$',wd): chunks.append([])
    chunks=[c for c in chunks if c]
    sil=sorted(sorted(sil,key=lambda s:s[0]-s[1])[:len(chunks)-1])
    bounds=[0]+[x for s in sil for x in s]+[d]
    segs=[(bounds[2*m],bounds[2*m+1]) for m in range(len(bounds)//2)]
    if len(segs)!=len(chunks): segs=[(0,d)]; chunks=[words]
    ws=[]
    for (a0,a1),c in zip(segs,chunks):
        tot=sum(len(re.sub(r'\W','',x))+1.5 for x in c); u=a0
        for x in c:
            dur=(len(re.sub(r'\W','',x))+1.5)/tot*(a1-a0)
            ws.append({'w':x,'s':round(t+u,3),'e':round(t+u+dur,3)}); u+=dur
    T.append({'text':l,'s':round(t,3),'e':round(t+d,3),'words':ws,'nseg':len(segs)})
    out.append(a); out.append(np.zeros(int(GAP[i]*SR))); t+=d+GAP[i]
a=np.concatenate(out)
w=wave.open('vo.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes())
json.dump({'lines':T,'voEnd':round(t,3)},open('timing.json','w'),indent=1)
for x in T: print(x['s'],x['e'],x['nseg'],x['text'])
print('end',t)
