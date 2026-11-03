"""Split script.txt into scenes of ~7-8 s at the locked voice speed (about 4 spoken syllables per second).
Cuts prefer sentence ends, then clause breaks (, ; :), then before a linking word; never mid-phrase unless forced."""
import re, json, sys, os, spoken
T, LO, HI = 30, 28, 32
import os
BAND = float(os.environ.get("BAND", 80)); CONJC = float(os.environ.get("CONJC", 25))
CONJ = {'and','but','so','while','because','which','when','who','where','after','until','including'}
GLUE = {'the','a','an','of','for','to','in','on','at','by','from','with','into','his','her','its','their','these','this','that','every','outer','inscribed','later','most','many','more','great','last','first','old','royal','was','were','is','had','has','have','be','been','could','would','will','built','took','called','named','than','as','who','which','and','or','but','so','while','because','when','where','after','until','including','about','around','like','nearly','almost','far','very','our','one','two','three','six','new','own','its','king','prince','general','emperor','lord','queen','god','great','Bronze','Middle','New','Old','Red','Black','Valley','Pyramid','Great','Seven','Mark','Julius','Howard','eastern','western','northern','southern','short-lived','powerful','huge','giant','massive','fine','white','black','single','largest','oldest','earliest','still','them','him','up','back','out','off','down','early','staged','recorded','strike','crushed','rebelled','again','gathered','hid','raised','brought','pyramid','king\'s','make','formal','across','land','see','walls','images','found','reigned','ruled','stood','changes','adopted','squeezed','way','sand','harvests','everything','archaeologists','afterlife','governors','trade','mines','soldiers','ptolemies','dynasty','horemheb','equals','rich','thebes','kings','taxes'}
text = open(os.environ.get('SRC', 'script.txt')).read().strip()
paras = [p.strip() for p in text.split('\n\n') if p.strip()]
words = []   # (word, break_cost_after, para_end)
for p in paras:
    ws = p.split()
    for i, wd in enumerate(ws):
        last = i == len(ws) - 1
        nxt = ws[i + 1].lower().strip('"') if not last else ''
        if last: cost = -6
        elif re.search(r'[.?!]"?$', wd): cost = 0
        elif re.search(r'[,;:]$', wd): cost = 8
        elif nxt in CONJ: cost = CONJC
        else: cost = float(os.environ.get("MID", 200))
        if not last and (wd.lower().strip('",') in GLUE or wd.strip('",') in GLUE or re.match(r'^[\d,.]+$', nxt) or nxt.upper().startswith('BC') or (wd[0].isupper() and nxt[:1].isupper() and not re.search(r'[.,;:?!]"?$', wd))):
            cost = 3000
        words.append((wd, cost, last))
SY = [spoken.stats(w)[1] for w, _, _ in words]
N = len(words); INF = 1e18
best = [INF] * (N + 1); prev = [-1] * (N + 1); best[0] = 0
for j in range(1, N + 1):
    n = 0
    for i in range(j - 1, -1, -1):
        n += SY[i]
        if n > HI + 12: break
        if n < LO - 12 and j < N: continue
        c = (n - T) ** 2 + words[j - 1][1]
        if j < N and n < LO: c += BAND * (LO - n)
        if n > HI: c += BAND * (n - HI)
        if best[i] + c < best[j]: best[j] = best[i] + c; prev[j] = i
cuts = []; j = N
while j > 0: cuts.append((prev[j], j)); j = prev[j]
cuts.reverse(); out = []
for i, j in cuts:
    t = ''
    for k in range(i, j):
        t += words[k][0] + (' // ' if words[k][2] and k < j - 1 else ' ')
    out.append(t.strip())
json.dump(out, open(os.environ.get('OUT', 'chunks.json'), 'w'), indent=0)
for i, s in enumerate(out, 1): print(i, spoken.stats(s)[1], s)
print(len(out), 'scenes', file=sys.stderr)
