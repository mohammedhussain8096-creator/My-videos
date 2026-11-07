import numpy as np, soundfile as sf, subprocess, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vs import S, FX, join, OUT, TMP, K
import numpy as np
V = np.load('/home/user/My-videos/istanbul/video/assets/kokoro/voices-v1.0.bin')
def kok(name, style, speed=0.92):
    ch = [K.create(s.replace('।', '.'), voice=style, speed=speed, lang='hi')[0] for s in S]; join(ch, 24000, f'{TMP}/{name}.wav')
kok('blend_omega_fenrir', 0.65 * V['hm_omega'] + 0.35 * V['am_fenrir'])
kok('blend_psi_onyx', 0.65 * V['hm_psi'] + 0.35 * V['am_onyx'])
kok('blend_omega_george', 0.6 * V['hm_omega'] + 0.4 * V['bm_george'])
kok('kokoro_hf_beta', 'hf_beta')
from piper import PiperVoice, SynthesisConfig
def pip(name, model, **cfg):
    pv = PiperVoice.load(f'piper/hi_IN-{model}-medium.onnx')
    ch = [np.concatenate([np.frombuffer(c.audio_int16_bytes, np.int16) for c in pv.synthesize(s, syn_config=SynthesisConfig(**cfg))]).astype(np.float32) / 32768 for s in S]
    join(ch, pv.config.sample_rate, f'{TMP}/{name}.wav')
pip('pratham_slow', 'pratham', length_scale=1.12)
pip('pratham_expr', 'pratham', length_scale=1.05, noise_scale=0.8, noise_w_scale=1.0)
pip('priyamvada', 'priyamvada', length_scale=1.05)
DEEP = ',equalizer=f=110:t=q:w=1:g=2.5'
ROOM = ',aecho=0.8:0.6:40|70:0.18|0.10'
jobs = [('8_pratham_slow', 'pratham_slow', FX + DEEP),
        ('9_pratham_deep_cinematic', 'pratham_slow', 'rubberband=pitch=0.94,' + FX + DEEP + ROOM),
        ('10_pratham_expressive', 'pratham_expr', FX + DEEP),
        ('11_blend_omega_fenrir', 'blend_omega_fenrir', FX + DEEP),
        ('12_blend_psi_onyx', 'blend_psi_onyx', FX + DEEP),
        ('13_blend_omega_george_deep', 'blend_omega_george', 'rubberband=pitch=0.92,' + FX + DEEP),
        ('14_female_kokoro_beta', 'kokoro_hf_beta', FX),
        ('15_female_piper_priyamvada', 'priyamvada', FX)]
for name, src, fx in jobs:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/{src}.wav', '-af', fx + ',loudnorm=I=-16:TP=-1.5', '-ar', '48000', '-b:a', '192k', f'{OUT}/{name}.mp3'], check=True)
    print(name)
