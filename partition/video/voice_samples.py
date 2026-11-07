import numpy as np, soundfile as sf, subprocess, wave, os, sys
OUT = '/home/user/My-videos/partition/voice_samples'; TMP = 'vs_tmp'; os.makedirs(TMP, exist_ok=True)
S = ['चौदह अगस्त, उन्नीस सौ सैंतालीस की रात।', 'दिल्ली की संविधान सभा में आधी रात का इंतज़ार हो रहा है।',
     'कुछ ही मिनटों में भारत आज़ाद होने वाला है।', 'लेकिन उसी रात, दिल्ली से कुछ ही घंटों की दूरी पर, पंजाब जल रहा था।',
     'गाँव के गाँव ख़ाली हो रहे थे।', 'यह कहानी है भारत के बँटवारे की।']
FX = 'highpass=f=60,equalizer=f=150:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5'
def join(chunks, sr, path):
    gap = np.zeros(int(0.45 * sr), np.float32)
    a = np.concatenate([np.concatenate([c.astype(np.float32), gap]) for c in chunks])
    sf.write(path, a, sr)
from kokoro_onnx import Kokoro
K = Kokoro('/home/user/My-videos/istanbul/video/assets/kokoro/kokoro-v1.0.onnx', '/home/user/My-videos/istanbul/video/assets/kokoro/voices-v1.0.bin')
if __name__ == '__main__':
    for v in ('hm_omega', 'hm_psi'):
        ch = [K.create(s.replace('।', '.'), voice=v, speed=0.92, lang='hi')[0] for s in S]; join(ch, 24000, f'{TMP}/{v}.wav')
    from piper import PiperVoice
    for v in ('rohan', 'pratham'):
        pv = PiperVoice.load(f'piper/hi_IN-{v}-medium.onnx')
        ch = []
        for s in S:
            a = np.concatenate([np.frombuffer(c.audio_int16_bytes, np.int16) for c in pv.synthesize(s)]).astype(np.float32) / 32768
            ch.append(a)
        join(ch, pv.config.sample_rate, f'{TMP}/piper_{v}.wav')
    jobs = [('1_kokoro_omega', 'hm_omega', FX), ('2_kokoro_omega_deep', 'hm_omega', 'rubberband=pitch=0.89,' + FX + ',equalizer=f=110:t=q:w=1:g=2.5'),
            ('3_kokoro_psi', 'hm_psi', FX), ('4_kokoro_psi_deep', 'hm_psi', 'rubberband=pitch=0.89,' + FX + ',equalizer=f=110:t=q:w=1:g=2.5'),
            ('5_piper_rohan', 'piper_rohan', 'atempo=0.95,' + FX), ('6_piper_pratham', 'piper_pratham', 'atempo=0.95,' + FX),
            ('7_piper_rohan_deep', 'piper_rohan', 'atempo=0.95,rubberband=pitch=0.9,' + FX + ',equalizer=f=110:t=q:w=1:g=2.5')]
    for name, src, fx in jobs:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/{src}.wav', '-af', fx + ',loudnorm=I=-16:TP=-1.5', '-ar', '48000', '-b:a', '192k', f'{OUT}/{name}.mp3'], check=True)
        print(name)
