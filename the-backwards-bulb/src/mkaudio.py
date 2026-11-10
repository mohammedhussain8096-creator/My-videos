import numpy as np, json, wave, re
SR=44100; T=json.load(open('timing.json')); Ls=T['lines']; DUR=T['voEnd']+0.9; N=int(DUR*SR)
rng=np.random.default_rng(7)
def wf(i,s,nth=1):
    n=0
    for w in Ls[i]['words']:
        if re.sub(r"[^a-z']",'',w['w'].lower()).startswith(s):
            n+=1
            if n==nth: return w['s']
    return Ls[i]['s']
CUT=lambda i: 0 if i==0 else Ls[i]['s']-0.1
mus=np.zeros(N); sfx=np.zeros(N)
def add(buf,t,x,g=1.0):
    i=int(t*SR)
    if i<0 or i>=N: return
    x=x[:N-i]; buf[i:i+len(x)]+=x*g
def env(n,a=0.005,d=8): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t*d)
def pluck(f,dur=0.5,d=9,h=(1,0.5,0.25,0.12)):
    n=int(dur*SR); t=np.arange(n)/SR; x=sum(a*np.sin(2*np.pi*f*(k+1)*t) for k,a in enumerate(h)); return x*env(n,0.003,d)
def noise(dur): return rng.standard_normal(int(dur*SR))
def lp(x,k):
    y=np.empty_like(x); a=0
    c=np.cumsum(x); y=(c-np.concatenate([np.zeros(k),c[:-k]]))/k; return y
mid=lambda m: 440*2**((m-69)/12)
# ---- music: sneaky pizzicato, 104 bpm ----
bpm=104; beat=60/bpm; bar=beat*4
prog=[[38,45,41,45],[38,45,41,44],[36,43,40,43],[33,40,45,44]]  # D minor walk
mel=[[62,None,65,None,69,None,65,64],[62,None,65,None,68,None,65,None],[60,None,64,None,67,None,64,62],[57,None,61,None,64,None,61,None]]
fin=CUT(14)
t=0; b=0
while t<DUR:
    major = t>=fin-0.01
    p=prog[b%4]; m=mel[b%4]
    for q in range(4):
        n=p[q]+(0 if not major else 0)
        add(mus,t+q*beat,pluck(mid(n),0.45,7,(1,0.6,0.2)),0.55)
        hat=noise(0.04)*env(int(0.04*SR),0.001,90); add(mus,t+q*beat+beat/2,hat-lp(hat,6),0.10)
    for e in range(8):
        if m[e] is not None:
            nn=m[e]+(1 if major and m[e]%12==5 else 0)  # F->F# in finale
            add(mus,t+e*beat/2,pluck(mid(nn+12),0.3,14,(1,0.3,0.1)),0.22)
    if b%2==1: add(mus,t+3.5*beat,pluck(mid(74),0.25,16),0.16)
    t+=bar; b+=1
# duck music under explainer slightly less; fade ends
fade=np.ones(N); k=int(0.4*SR); fade[:k]=np.linspace(0,1,k); k2=int(0.7*SR); fade[-k2:]=np.linspace(1,0,k2); mus*=fade
# ---- sfx ----
def whoosh(d=0.28):
    n=int(d*SR); x=lp(noise(d),40); e=np.sin(np.linspace(0,np.pi,n))**2; return x*e*6
def pop(f=520):
    n=int(0.09*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*(f+f*1.2*t/0.09)*t)*env(n,0.002,30)
def bonk():
    n=int(0.45*SR); t=np.arange(n)/SR; f=180*np.exp(-t*7)+70; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
    wood=np.sin(2*np.pi*820*t)*np.exp(-t*40)*0.5; return x+wood
def boing():
    n=int(0.5*SR); t=np.arange(n)/SR; f=300+140*np.sin(2*np.pi*11*t)*np.exp(-t*4); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)*0.6
def squeak(d=0.22,f0=1400,f1=2100):
    n=int(d*SR); t=np.arange(n)/SR; f=np.linspace(f0,f1,n)+60*np.sin(2*np.pi*35*t); x=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*0.25+np.sin(2*np.pi*np.cumsum(f)/SR); return x*np.sin(np.linspace(0,np.pi,n))**0.7*0.35
def metal(fs,d=5,dur=0.8):
    n=int(dur*SR); t=np.arange(n)/SR; return sum(np.sin(2*np.pi*f*t)*np.exp(-t*(d+i*1.5)) for i,f in enumerate(fs))/len(fs)
def click(): n=int(0.03*SR); x=noise(0.03)*env(n,0.0005,160); return x-lp(x,5)
def sweep(f0,f1,d):
    n=int(d*SR); t=np.arange(n)/SR; f=f0*(f1/f0)**(t/d); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.linspace(0,np.pi,n))**0.5
for i in range(1,len(Ls)): add(sfx,CUT(i)-0.12,whoosh(),0.5)
P=lambda t,f=520,g=0.35: add(sfx,t,pop(f),g)
tb=wf(0,'beaten')-0.05
P(0.35); add(sfx,tb-0.1,whoosh(),0.6); add(sfx,tb+0.28,bonk(),0.9); add(sfx,tb+0.3,boing(),0.5); P(wf(0,'light'),700)
P(CUT(1)+0.25); P(CUT(1)+0.55,650); add(sfx,wf(1,'and')-0.15,whoosh(),0.5); P(wf(1,'never'),700)
for q in range(4): add(sfx,CUT(2)+0.25+q*0.3,squeak(0.2,1300+q*120,1900+q*150),0.5)
P(CUT(2)+0.1); P(wf(2,'one',2),650); add(sfx,wf(2,'straight')+0.1,sweep(300,900,0.25),0.25); P(wf(2,'straight')+0.4,800)
P(CUT(3)+0.3)
for q in range(5): add(sfx,wf(3,'half')+q*0.22,squeak(0.18,1200+q*90,1800+q*100),0.35)
P(wf(3,'half'),650)
for q in range(4): add(sfx,CUT(4)+0.15+q*0.28,click(),0.9); 
add(sfx,wf(4,'dark')-0.15,sweep(500,60,0.7),0.4); P(wf(4,'dark'),300,0.3)
P(wf(5,'guards')); add(sfx,wf(5,'lenny')+0.1,sweep(400,800,0.2),0.2); add(sfx,wf(5,'lenny')+0.35,metal([1320,1980,2640],6,0.6),0.25)
for q in range(2): add(sfx,wf(5,'and')+0.3+q*0.45,sweep(160,110,0.4),0.3)
add(sfx,CUT(6)+0.6,metal([523,811,1244,1790,2417],6,0.9),0.7); P(wf(6,'cages'))
tp=wf(6,'pliers'); add(sfx,tp,click(),1.4); add(sfx,tp+0.07,click(),1.2); add(sfx,tp+0.45,metal([400,640,990],9,0.5),0.4)
idea=wf(7,'changed')-0.05; add(sfx,idea,metal([1318,1976,2637],4,1.1),0.55); P(wf(7,'one'),600); P(wf(7,'thing'),760)
P(wf(8,'like'),650)
a=wf(9,'it')-0.05; b=wf(9,'he',2)-0.05; c=wf(9,'it',2)-0.05; s9=CUT(9)
for q in range(2): add(sfx,s9+0.12+q*0.25,squeak(0.2,1300,1900),0.5)
for q in range(3): add(sfx,a+0.08+q*0.2,pluck(260-q*20,0.15,20),0.4)
for q in range(int((c-b)/0.14)): add(sfx,b+0.08+q*0.14,squeak(0.12,1500+(q%2)*300,2200+(q%2)*300),0.5)
add(sfx,c+0.05,sweep(900,300,0.38),0.25); add(sfx,c+0.42,bonk(),1.0); add(sfx,c+0.44,boing(),0.55)
P(wf(10,'every'),600); add(sfx,wf(10,'tightens')-0.1,squeak(0.5,700,1100),0.25); P(wf(10,'right')-0.25,760); add(sfx,CUT(11)-0.4,metal([1760,2637],5,0.5),0.3)
P(wf(11,'threads'),600); tf=wf(11,'backwards')-0.08; add(sfx,tf,sweep(1500,300,0.3),0.4); add(sfx,tf+0.05,whoosh(0.35),0.9); P(tf+0.1,820,0.4)
P(CUT(12)+0.05,650); add(sfx,CUT(12)+0.2,squeak(0.5,700,1150),0.25); tR=wf(12,'right')-0.08; add(sfx,tR-0.3,metal([1760,2637],5,0.5),0.3); P(tR,500); add(sfx,tR+0.3,sweep(900,150,0.6),0.35); add(sfx,min(CUT(13)-0.25,tR+0.95),bonk(),0.6)
s13=CUT(13); add(sfx,s13+0.3,sweep(300,600,0.5),0.15); add(sfx,s13+1.45,click(),1.6); add(sfx,s13+1.5,metal([900,1500,2300],10,0.3),0.5); P(wf(13,'key'),600); P(wf(13,'one'),700); P(wf(13,'own'),300,0.35)
P(wf(14,'stealing'),600); P(wf(14,'stopped'),780); add(sfx,wf(14,'stopped')+0.05,metal([1046,1318,1568,2093],3,1.2),0.35)
P(CUT(15)+0.12,420); tb15=wf(15,'he')-0.05; s16=CUT(16); P(wf(15,'first'),600); P(wf(15,'ticket'),760); add(sfx,tb15+0.6*(s16-tb15),metal([3100,4650,6200],7,0.7),0.6)
P(wf(16,'he'),600); P(wf(16,'light'),820); 
for q,nn in enumerate([74,78,81,86]): add(sfx,wf(16,'light')+0.1+q*0.09,pluck(mid(nn),0.9,4,(1,0.3)),0.3)
# ---- voice ----
w=wave.open('vo.wav'); v=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
v=np.interp(np.arange(0,len(v),22050/SR),np.arange(len(v)),v); vo=np.zeros(N); vo[:min(N,len(v))]=v[:N]
vo/=np.abs(vo).max(); 
# sidechain: duck music when voice active
e=lp(np.abs(vo),int(0.08*SR)); duck=1-0.45*np.clip(e/0.08,0,1)
mix=vo*0.92 + mus/np.abs(mus).max()*0.2*duck + sfx*0.32
mix=np.tanh(mix*1.15)/np.tanh(1.15); mix*=0.95/np.abs(mix).max()
o=wave.open('mix.wav','w'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix*32767).astype(np.int16).tobytes()); print('ok',DUR)
