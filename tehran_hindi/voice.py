"""Generate the Hindi voice-over line by line and write timings.json.

Usage: python voice.py <script.json> <out_dir> [ca_bundle]
"""
import asyncio
import json
import ssl
import subprocess
import sys

import edge_tts
import edge_tts.communicate as comm

VOICE, RATE, PITCH = "hi-IN-MadhurNeural", "+18%", "-4Hz"
GAP = 0.3  # breathing room after each line (s)


async def main(script, out, ca):
    if ca:
        comm._SSL_CTX = ssl.create_default_context(cafile=ca)
    lines = json.load(open(script))
    timings = []
    for ln in lines:
        mp3 = f"{out}/{ln['id']}.mp3"
        await edge_tts.Communicate(ln["text"], VOICE, rate=RATE, pitch=PITCH).save(mp3)
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", mp3]).decode())
        timings.append(dict(id=ln["id"], scene=ln["scene"], voice=mp3, vdur=d, dur=round(d + GAP, 3)))
        print(ln["id"], round(d, 2), flush=True)
    timings[-1]["dur"] += 1.5  # let the final shot breathe
    json.dump(timings, open(f"{out}/timings.json", "w"), indent=1)


asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
