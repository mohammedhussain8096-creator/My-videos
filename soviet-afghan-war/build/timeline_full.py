import re, json
gaps=[0.5,0.8,0.4,0.5,0.9,0.5,1.0,0.9,0.4,0.6,0.4,0.4,0.7,0.6,0.5,0.9,0.4,0.5,0.9,0.5,0.6,0.5,0.6,0.8,0.6,2.5]
dur={l.split()[0]:float(l.split()[1]) for f in ("vo/trim.txt","vo/trim_rest.txt") for l in open(f) if l.startswith("s")}
gaps[25]=1.6
X={27:.5,33:.6,35:.4,38:.9,40:.9,41:.6,43:.4,45:.5,47:.5,48:.8,53:.9,54:.6,56:.5,58:.9,59:.6,63:.8,67:.4,70:.8,73:.6,74:.4,76:.6,82:.6,85:.9,88:.8,90:.6,92:.4,94:.9,95:.6,96:.6,99:.8,100:.4,101:.9,103:.6,104:1.3,105:.9,106:.8,107:3.5}
X.update({28:.1,34:1.0,51:.8,65:1.0,70:1.4,71:.8,76:.8,78:1.8,81:.8,82:.8,95:1.3,96:.3,97:.4,99:1.0,41:.5,43:.3,54:.8,55:.3,79:.8,86:.4,104:1.0})
gaps+= [X.get(i,0.5) for i in range(27,108)]
def ts(s):
    h,m,r=s.split(":"); sec,ms=r.split(","); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
t=0.6; lines=[]
for i in range(1,108):
    k=f"s{i:02d}"; srt=open(f"vo/{k}.mp3.srt").read()
    words=[(ts(a),ts(b),w.strip()) for a,b,w in re.findall(r"(\S+) --> (\S+)\n(.+?)\n",srt)]
    lead=words[0][0]
    words=[(round(t+a-lead,3),round(t+b-lead,3),w) for a,b,w in words]
    lines.append(dict(k=k,start=round(t,3),end=round(t+dur[k],3),words=words))
    t+=dur[k]+gaps[i-1]
json.dump(dict(lines=lines,total=round(t,3)),open("timeline_full.json","w"),indent=1)
for L in lines[26:]: print(L["k"],L["start"],L["end"], " ".join(f'{w}@{a}' for a,b,w in L["words"]))
print("total",t)
