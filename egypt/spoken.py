import re
ONES="zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS="_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def n2w(n):
    if n<20: return ONES[n]
    if n<100: return TENS[n//10]+('-'+ONES[n%10] if n%10 else '')
    if n<1000: return ONES[n//100]+' hundred'+(' and '+n2w(n%100) if n%100 else '')
    if n<1_000_000: return n2w(n//1000)+' thousand'+(' '+n2w(n%1000) if n%1000 else '')
    return n2w(n//1_000_000)+' million'+(' '+n2w(n%1_000_000) if n%1_000_000 else '')
def year(n):
    if n<1000 or n%1000<10 and n%100==0 and n<2000 and n%1000==0: return n2w(n)
    if n%100==0: return n2w(n//100)+' hundred'
    return n2w(n//100)+' '+(n2w(n%100) if n%100>=10 else 'oh-'+n2w(n%100))
ROMAN={'II':'the second','III':'the third','IV':'the fourth','V':'the fifth','VII':'the seventh','I':'the first'}
def expand(t):
    t=t.replace('//','')
    t=re.sub(r'(\d+(?:\.\d+)?) million',lambda m:(m.group(1).replace('.',' point ').replace('2','two').replace('3','three'))+' million',t)
    t=re.sub(r'\b(\d{3,4})s\b',lambda m:year(int(m.group(1)))+'s',t)
    t=re.sub(r'\bAD (\d{1,4})\b',lambda m:'A D '+year(int(m.group(1))),t)
    t=re.sub(r'\b(\d{1,4}) BC\b',lambda m:year(int(m.group(1)))+' B C',t)
    t=re.sub(r'\b(\d{4})\b(?!,\d)',lambda m:year(int(m.group(1))) if 1800<int(m.group(1))<2100 else n2w(int(m.group(1))),t)
    t=re.sub(r'\b(\d{1,3}),(\d{3})\b',lambda m:n2w(int(m.group(1)+m.group(2))),t)
    t=re.sub(r'\b\d+\b',lambda m:n2w(int(m.group(0))),t)
    t=re.sub(r'\b(Pepi|Mentuhotep|Thutmose|Amenhotep|Ramesses|Psamtik|Necho|Darius|Nectanebo|Ptolemy|Cleopatra) (I{1,3}|IV|V|VII)\b',lambda m:m.group(1)+' '+ROMAN[m.group(2)],t)
    return t
def syl(w):
    w=re.sub(r'[^a-z]','',w.lower())
    if not w: return 0
    g=len(re.findall(r'[aeiouy]+',w))
    if w.endswith('e') and not w.endswith(('le','ee')) and g>1: g-=1
    return max(1,g)
def stats(t):
    e=expand(t); ws=e.replace('-',' ').split()
    return len(ws), sum(syl(w) for w in ws)
