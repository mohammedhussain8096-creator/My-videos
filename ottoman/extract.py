"""Ottoman_Script.md -> narration.json (one entry per paragraph; the ## heading is kept as the part name)."""
import json, re, sys
out, part = [], ''
for block in open(sys.argv[1], encoding='utf-8').read().split('\n\n'):
    b = block.strip()
    if not b or b.startswith('# '): continue
    if b.startswith('## '): part = b[3:].strip(); continue
    out.append({'part': part, 'cue': '', 'text': ' '.join(b.split())})
json.dump(out, open('narration.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'paragraphs,', sum(len(o['text'].split()) for o in out), 'words')
