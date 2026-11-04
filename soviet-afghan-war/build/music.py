import numpy as np, json, sys, wave
SR=48000
T=float(sys.argv[1]); hits=[float(x) for x in sys.argv[2].split(",")]
N=int(T*SR); t=np.arange(N)/SR
rng=np.random.default_rng(7)
def lp(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(f/fc)**4); return np.fft.irfft(X,len(x))
def note(m): return 440*2**((m-69)/12)
def saw(fr,ph=0): return 2*((t*fr+ph)%1)-1
chords=[[38,50,53,57],[34,46,50,53],[31,43,50,55],[33,45,52,57]]  # Dm Bb Gm A
L=8.0
pad=np.zeros(N)
for ci in range(int(T/L)+2):
    ch=chords[ci%4]; s0=ci*L; env=np.clip(1-np.abs((t-s0-L/2)/(L*0.62)),0,1)**1.5
    m=env>0
    for n in ch:
        for det in (-0.08,0.0,0.07):
            pad[m]+=saw(note(n)*(1+det/100*12/12*0.01)+det)[m]*env[m]*0.06
pad=lp(pad,700)
sub=np.zeros(N)
for ci in range(int(T/L)+2):
    s0=ci*L; env=np.clip(1-np.abs((t-s0-L/2)/(L*0.62)),0,1); sub+=np.sin(2*np.pi*note(chords[ci%4][0]-12)*t)*env*0.25
# heartbeat pulse every 1.6s starting 30s, low
pulse=np.zeros(N)
for st in np.arange(28,T-3,1.6):
    for off,a in ((0,1),(0.22,0.6)):
        i=int((st+off)*SR); n=int(0.35*SR)
        if i+n>N: continue
        tt=np.arange(n)/SR; pulse[i:i+n]+=np.sin(2*np.pi*(55-20*tt/0.35)*tt)*np.exp(-tt*14)*a*0.5
# impacts
imp=np.zeros(N)
for h in hits:
    i=int(h*SR); n=int(3.5*SR); n=min(n,N-i); tt=np.arange(n)/SR
    boom=np.sin(2*np.pi*(70*np.exp(-tt*3)+28)*tt)*np.exp(-tt*1.6)
    nz=lp(rng.normal(0,1,n),900)*np.exp(-tt*5)*0.6
    imp[i:i+n]+=(boom+nz)*0.9
    # reverse whoosh before hit
    w=int(1.2*SR); j=max(0,i-w); ww=i-j; tw=np.arange(ww)/SR
    imp[j:i]+=lp(rng.normal(0,1,ww),2500)*(tw/1.2)**3*0.35
# air / wind
air=lp(rng.normal(0,1,N),400)*0.05*(1+0.5*np.sin(2*np.pi*t/11))
mix=pad+sub+pulse*0.8+imp+air
fade=np.clip(t/2.5,0,1)*np.clip((T-t)/3.0,0,1); mix*=fade
mix/=np.max(np.abs(mix))*1.05
st=np.stack([mix, np.roll(mix,int(0.012*SR))],1)
d=(st*32767).astype(np.int16)
w=wave.open(sys.argv[3],"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close()
