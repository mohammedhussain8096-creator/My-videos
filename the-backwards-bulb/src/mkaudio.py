import numpy as np, json, wave, re, soundfile as sf
SR=44100; T=json.load(open('timing.json')); Ls=T['lines']; DUR=T['voEnd']+0.9; N=int(DUR*SR)
S='../sep/'
def wf(i,s,nth=1):
    n=0
    for w in Ls[i]['words']:
        if re.sub(r"[^a-z']",'',w['w'].lower()).startswith(s):
            n+=1
            if n==nth: return w['s']
    return Ls[i]['s']
CUT=lambda i: 0 if i==0 else Ls[i]['s']-0.1
src={n:sf.read(S+f'{n}_sfx.wav')[0] for n in ['coins','carp']}
def clip(n,t0,t1,pre=0.03,tail=0.12):
    a=src[n][int((t0-pre)*SR):int((t1+tail)*SR)].copy(); f=int(0.012*SR); g=int(tail*SR)
    a[:f]*=np.linspace(0,1,f); a[-g:]*=np.linspace(1,0,g)**2; return a/ (np.abs(a).max()+1e-9)
def pitch(a,r): return np.interp(np.arange(0,len(a),r),np.arange(len(a)),a)
SQ=[clip('carp',8.95,9.35),clip('carp',16.10,16.70),clip('carp',46.65,47.30)]
SCRAPE=clip('coins',0.25,0.70); CLINK=clip('coins',37.95,38.75,tail=0.25); BANG=clip('coins',27.20,27.45,tail=0.3)
THUD=clip('coins',20.00,20.25,tail=0.2); CREAK=clip('coins',55.40,55.90,tail=0.2); SLIDE=clip('carp',36.40,36.95,tail=0.2); DING=clip('carp',13.05,13.40,tail=0.25)
sfx=np.zeros(N)
def add(t,x,g=1.0):
    i=int(t*SR)
    if 0<=i<N: x=x[:N-i]; sfx[i:i+len(x)]+=x*g
tb=wf(0,'beaten')-0.05
add(tb+0.26,THUD,1.0)                                   # bulb bonks his head
add(CUT(2)+0.35,SQ[0],0.8)                              # one twist
add(wf(3,'half')+0.05,SQ[1],0.7)                        # everybody twisting
add(CUT(6)+0.58,BANG,0.9)                               # cage slams down
add(wf(6,'pliers'),SCRAPE,0.8)                          # pliers
add(wf(7,'changed')-0.05,DING,0.8)                      # idea
add(CUT(8)+0.15,CREAK,0.7)                              # walks in at home
s9=CUT(9); b=wf(9,'he',2)-0.05; c=wf(9,'it',2)-0.05
add(s9+0.15,SQ[2],0.75); add(b+0.1,pitch(SQ[0],1.12),0.8); add(b+0.55,pitch(SQ[0],1.25),0.8)
add(c+0.40,THUD,1.0)                                    # bulb lands on foot
add(wf(11,'backwards')-0.1,SLIDE,0.8)                   # thread flips
add(CUT(12)+0.25,pitch(SQ[1],0.9),0.6)                  # screws in
add(min(CUT(13)-0.3,wf(12,'right')+0.9),THUD,0.6)       # falls out
tb15=wf(15,'he')-0.05; add(tb15+0.6*(CUT(16)-tb15),CLINK,0.9)   # coin at ticket booth
# ---- music bed: the channel's own track, aligned so its ending lands on ours ----
m=sf.read(S+'coins_music.wav')[0]; m=m[len(m)-N:] if len(m)>=N else np.pad(m,(N-len(m),0))
f=int(0.6*SR); m[:f]*=np.linspace(0,1,f); g=int(0.5*SR); m[-g:]*=np.linspace(1,0,g)
# ---- voice ----
w=wave.open('vo.wav'); v=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
v=np.interp(np.arange(0,len(v),22050/SR),np.arange(len(v)),v); vo=np.zeros(N); vo[:min(N,len(v))]=v[:N]; vo/=np.abs(vo).max()
# match the reference's voice-to-bed balance
rv=sf.read(S+'out/htdemucs/coins/vocals.wav')[0].mean(1); rb=sf.read(S+'out/htdemucs/coins/no_vocals.wav')[0].mean(1)
rms=lambda x: np.sqrt((x[np.abs(x)>1e-3]**2).mean())
ratio=rms(rb)/rms(rv); print('reference bed/voice ratio dB',20*np.log10(ratio))
bed=m+0; mg=rms(vo)*ratio/rms(bed)*0.9
ref_sfx_peak=np.abs(src['coins']).max()/np.abs(rv).max()
mix=vo*0.9+bed*mg*0.9+sfx*min(0.5,ref_sfx_peak)*0.9
mix=np.tanh(mix*1.1)/np.tanh(1.1); mix*=0.95/np.abs(mix).max()
sf.write('mix2.wav',mix,SR); print('ok',DUR,'music gain',mg,'sfx gain',min(0.5,ref_sfx_peak))
