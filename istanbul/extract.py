"""Pull the spoken narration out of the script .docx (skips the title block and the (Audio: ...) notes,
which are kept as the music cue for the paragraphs that follow). Writes narration.json."""
import json, re, sys, docx
d = docx.Document(sys.argv[1])
out, cue, started = [], '', False
for p in d.paragraphs:
    t = p.text.strip()
    if not t: continue
    if t.lower().startswith('narration'): started = True; continue
    if not started: continue
    if t.startswith('(Audio'): cue = re.sub(r'^\(Audio:\s*|\)$', '', t); continue
    out.append({'part': '', 'cue': cue, 'text': t})
json.dump(out, open('narration.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'paragraphs,', sum(len(o['text'].split()) for o in out), 'words')
