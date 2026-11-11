#!/bin/bash
# One-time setup in a fresh session. Run from the pipeline/ folder.
set -e
npm i three@0.160.0
pip install -q piper-tts faster-whisper librosa soundfile numpy
mkdir -p voice music sfx
[ -s voice/en_US-ryan-high.onnx ] || for f in en_US-ryan-high.onnx en_US-ryan-high.onnx.json; do curl -sSL -o voice/$f https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/$f; done
# Music: Kevin MacLeod, CC-BY 4.0 (credit required in the video description)
for n in "Cool%20Vibes" "Bass%20Walker" "Backbay%20Lounge" "Investigations"; do f=music/$(echo $n | sed 's/%20/_/g').mp3; [ -s "$f" ] || curl -sSL -A 'Mozilla/5.0' -o "$f" "https://incompetech.com/music/royalty-free/mp3-royaltyfree/$n.mp3"; done
# Sound effects: Kenney, CC0. The site hands out a signed link per download.
for p in impact-sounds interface-sounds sci-fi-sounds; do
  [ -d sfx/$p ] && continue
  curl -sS -A 'Mozilla/5.0' -c cj "https://kenney.nl/assets/$p" -o page.html
  id=$(grep -oE "data-download-id='[0-9a-f]+'" page.html | head -1 | cut -d"'" -f2)
  u=$(curl -sS -A 'Mozilla/5.0' -b cj -e "https://kenney.nl/assets/$p" -H 'Accept: application/json' "https://kenney.nl/download-link/$id" | python3 -c "import sys,json;print(json.load(sys.stdin)['url'])")
  mkdir -p sfx/$p && curl -sSL -A 'Mozilla/5.0' -b cj -o sfx/$p.zip "$u" && (cd sfx/$p && unzip -oq ../$p.zip) && rm sfx/$p.zip
done
rm -f cj page.html; echo "setup done"
