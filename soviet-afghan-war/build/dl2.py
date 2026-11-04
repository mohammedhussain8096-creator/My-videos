import time, sys, urllib.request, urllib.parse, urllib.error, os
UA={"User-Agent":"MyVideosDocBuilder/1.0 (https://github.com/mohammedhussain8096-creator/My-videos)"}
for line in open(sys.argv[2]):
    if not line.strip(): continue
    key,title=line.strip().split("|",1)
    fn=f"{sys.argv[1]}/{key}.jpg"
    if os.path.exists(fn) and os.path.getsize(fn)>10000: continue
    f=title.split(":",1)[1].replace(" ","_")
    u="https://commons.wikimedia.org/w/thumb.php?"+urllib.parse.urlencode(dict(f=f,w=1920))
    for a in range(5):
        try:
            d=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read(); break
        except urllib.error.HTTPError as e:
            print(key,"err",e.code,flush=True); d=None
            if e.code==429: time.sleep(20*(a+1))
            else: break
    if d: open(fn,"wb").write(d); print(key,len(d),flush=True)
    time.sleep(3)
