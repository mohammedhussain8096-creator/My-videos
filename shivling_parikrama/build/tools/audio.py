import json, sys, numpy as np, soundfile as sf
SR=44100
cues=json.load(open(sys.argv[1])); vo,vsr=sf.read(sys.argv[2],dtype='float32'); out=sys.argv[3]
N=int(cues['end']*SR)+SR; rng=np.random.default_rng(7)
t=np.arange(N)/SR
def env(n,a,d):  # attack secs, exp decay secs
    x=np.arange(n)/SR; e=np.minimum(1,x/max(a,1e-4))*np.exp(-x/d); return e
def place(buf,sig,at,g=1.0):
    i=int(at*SR); 
    if i>=len(buf): return
    j=min(len(buf),i+len(sig)); buf[i:j]+=sig[:j-i]*g
from scipy.signal import lfilter
def lp(x,a): return lfilter([a],[1,-(1-a)],x).astype(np.float32)
music=np.zeros(N,np.float32); sfx=np.zeros(N,np.float32)
# --- tanpura drone (D): Pa Sa Sa Sa(low) plucks every 0.65s, rich harmonics
base={'P':110.0,'S':146.83,'s':73.42}
seq=['P','S','S','s']; dur=4.0
pl=int(dur*SR); x=np.arange(pl)/SR
def pluck(f):
    s=np.zeros(pl)
    for h in range(1,14):
        amp=(1/h)*(1.0 if h%2 else .8)*np.exp(-x*(0.35+h*0.09))
        s+=amp*np.sin(2*np.pi*f*h*x*(1+0.0007*h)+h)
    return (s*np.minimum(1,x/0.02)).astype(np.float32)
P={k:pluck(f) for k,f in base.items()}
k=0; tt=0.0
while tt<cues['end']+1: place(music,P[seq[k%4]],tt,0.05); k+=1; tt+=0.65
# --- pad: D A D F# (soft), slow swell with LFO
for f,g in [(293.66,.022),(440.0,.016),(587.33,.012),(369.99,.010),(220.0,.018)]:
    music+= (g*np.sin(2*np.pi*f*t+np.sin(2*np.pi*.13*t)*.6)*(0.6+0.4*np.sin(2*np.pi*.05*t+f))).astype(np.float32)
# section mood: darker pad dip in sc7 / louder at end
scen={s['id']:s for s in cues['scenes']}
def ramp(a,b,v0,v1):
    g=np.ones(N,np.float32); i,j=int(a*SR),int(b*SR); g[:i]=v0; g[i:j]=np.linspace(v0,v1,j-i); g[j:]=v1; return g
m=np.ones(N,np.float32)
a7,b7=scen['sc7']['a'],scen['sc7']['b']; m*=np.where((t>a7)&(t<b7),0.45,1.0).astype(np.float32)
m*=ramp(cues['end']-2.5,cues['end'],1,0)*ramp(0,1.0,0.0,1.0)
music*=m
# --- bell
def bell(f=520,d=3.5,g=1):
    n=int((d+1)*SR); x=np.arange(n)/SR; s=np.zeros(n)
    for r,a,dd in [(1,1,d),(2.76,.5,d*.6),(5.40,.3,d*.35),(8.93,.15,d*.2),(0.5,.35,d*1.2)]:
        s+=a*np.sin(2*np.pi*f*r*x)*np.exp(-x/dd)
    return (s*np.minimum(1,x/0.004)*g).astype(np.float32)
for at in [0.05]+[scen[i]['a'] for i in ['sc4','tc1','tc2','tc3','sc9','sc10']]: place(sfx,bell(),at+.05,.16)
# --- whoosh at scene starts
def whoosh(d=.7):
    n=int(d*SR); w=rng.standard_normal(n).astype(np.float32); w=lp(w,0.08)-lp(w,0.01)
    e=np.sin(np.linspace(0,np.pi,n))**2; return (w*e).astype(np.float32)
W=whoosh(); W=lp(W,0.35)  # softer top end
WG=float(sys.argv[6]) if len(sys.argv)>6 else 0.45
WAT=float(sys.argv[7]) if len(sys.argv)>7 else 0.07
for s in cues["scenes"][1:]: place(sfx,W,max(0,s["a"]-.45),WG)
# --- shimmer for gold, pop for tags
def chime():
    n=int(1.6*SR); x=np.arange(n)/SR; s=np.zeros(n)
    for i,f in enumerate([1318.5,1760,2349.3,2637]):
        d=i*0.06; xi=np.clip(x-d,0,None); s+=np.where(x>d,np.sin(2*np.pi*f*xi)*np.exp(-xi/0.5),0)*.25
    return s.astype(np.float32)
def pop():
    n=int(.25*SR); x=np.arange(n)/SR; f=220*np.exp(-x*18)+160
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x/0.06)).astype(np.float32)
CH,PO=chime(),pop()
for o in cues['ov']:
    if o['kind']=='gold': place(sfx,CH,o['a']-.05,.35)
    if o['kind']=='tag': place(sfx,PO,o['a']-.08,.55)
# --- water
for a,b in cues['water']:
    n=int((b-a)*SR); w=rng.standard_normal(n).astype(np.float32); w=lp(w,0.25)-lp(w,0.05)
    mod=0.6+0.4*np.abs(np.sin(np.arange(n)/SR*9))*np.abs(np.sin(np.arange(n)/SR*3.7))
    e=np.minimum(1,np.minimum(np.arange(n)/(.4*SR),(n-np.arange(n))/(.4*SR)))
    place(sfx,(w*mod*e).astype(np.float32),a,WAT)
# --- footsteps (step every ~0.42s)
def step():
    n=int(.12*SR); x=np.arange(n)/SR; w=rng.standard_normal(n); w=lp(w.astype(np.float32),0.15)
    return (w*np.exp(-x/0.025)).astype(np.float32)
for a,b in cues['walks']:
    tt=a+.2
    while tt<b: place(sfx,step(),tt,.55); tt+=0.42
# --- final mix
vo=np.interp(np.arange(int(len(vo)*SR/vsr))*vsr/SR,np.arange(len(vo)),vo).astype(np.float32)
V=np.zeros(N,np.float32); V[:len(vo)]=vo[:N]
# ducking: music lower while voice present
envv=np.convolve(np.abs(V),np.ones(4410)/4410,mode='same'); duck=np.where(envv>0.01,0.55,1.0).astype(np.float32)
duck=np.convolve(duck,np.ones(8820)/8820,mode='same').astype(np.float32)
MG=float(sys.argv[4]) if len(sys.argv)>4 else 1.0; SG=float(sys.argv[5]) if len(sys.argv)>5 else .8
sf.write(out.replace('.wav','_music.wav'),music*duck*MG,SR); sf.write(out.replace('.wav','_sfx.wav'),sfx*SG,SR)
mix=V*1.0+music*duck*MG+sfx*SG
sf.write(out,np.stack([mix,mix],1),SR)
print('ok',N/SR)
