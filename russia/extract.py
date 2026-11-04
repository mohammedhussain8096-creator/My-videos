"""Pull the spoken narration out of the script .docx, keeping each part's heading and the
[ON SCREEN] cue that applies to each paragraph. Writes narration.json."""
import json, re, sys, docx
src = sys.argv[1]
d = docx.Document(src)
out, part, cue, started = [], '', '', False
for p in d.paragraphs:
    t = p.text.strip()
    if not t: continue
    if p.style.name.startswith('Heading 2'):
        if re.match(r'\d+:\d+', t): started = True; part = t.split('—', 1)[-1].strip()
        continue
    if not started or p.style.name.startswith('Heading'): continue
    m = re.match(r'\[(?:ON SCREEN:)?\s*(.*)\]$', t)
    if m: cue = m.group(1); continue
    out.append({'part': part, 'cue': cue, 'text': t})
json.dump(out, open('narration.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'paragraphs,', sum(len(o['text'].split()) for o in out), 'words')
