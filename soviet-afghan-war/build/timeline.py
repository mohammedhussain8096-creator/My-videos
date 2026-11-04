import re, json
gaps=[0.5,0.8,0.4,0.5,0.9,0.5,1.0,0.9,0.4,0.6,0.4,0.4,0.7,0.6,0.5,0.9,0.4,0.5,0.9,0.5,0.6,0.5,0.6,0.8,0.6,2.5]
dur={l.split()[0]:float(l.split()[1]) for l in open("vo/trim.txt")}
def ts(s):
    h,m,r=s.split(":"); sec,ms=r.split(","); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
t=0.6; lines=[]
for i in range(1,27):
    k=f"s{i:02d}"; srt=open(f"vo/{k}.mp3.srt").read()
    words=[(ts(a),ts(b),w.strip()) for a,b,w in re.findall(r"(\S+) --> (\S+)\n(.+?)\n",srt)]
    lead=words[0][0]
    words=[(round(t+a-lead,3),round(t+b-lead,3),w) for a,b,w in words]
    lines.append(dict(k=k,start=round(t,3),end=round(t+dur[k],3),words=words))
    t+=dur[k]+gaps[i-1]
json.dump(dict(lines=lines,total=round(t,3)),open("timeline.json","w"),indent=1)
for L in lines: print(L["k"],L["start"],L["end"], " ".join(f'{w}@{a}' for a,b,w in L["words"]))
print("total",t)
