import math, base64
INK='#1b1522'
def gear(cx,cy,r,teeth,depth):
    pts=[]
    for i in range(teeth*4):
        a=i/(teeth*4)*2*math.pi - math.pi/2
        rr = r+depth if i%4 in (1,2) else r
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return 'M '+' L '.join(pts)+' Z'
def hexa(cx,cy,r):
    return 'M '+' L '.join(f'{cx+r*math.cos(math.pi/6+i*math.pi/3):.1f},{cy+r*math.sin(math.pi/6+i*math.pi/3):.1f}' for i in range(6))+' Z'
def arc(cx,cy,r,a0,a1):
    p=lambda a:(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
    x0,y0=p(a0);x1,y1=p(a1); large=1 if (a1-a0)%360>180 else 0
    return f'M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}'
def glowstroke(d,col,w,fill='none'):
    return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w*1.6}" filter="url(#soft)" opacity="0.75"/><path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}"/>'
def body(col1,col2,extra=''):
    return f'''<linearGradient id="coat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col1}"/><stop offset="1" stop-color="{col2}"/></linearGradient>''','''
    <path d="M 232 1100 C 232 860 330 742 512 742 C 694 742 792 860 792 1100 Z" fill="url(#coat)" stroke="#1b1522" stroke-width="24"/>'''+extra
HEAD='''<circle cx="512" cy="478" r="238" fill="url(#skin)" stroke="#1b1522" stroke-width="24"/>
    <ellipse cx="372" cy="566" rx="38" ry="26" fill="#f08a7a" opacity="0.45"/><ellipse cx="652" cy="566" rx="38" ry="26" fill="#f08a7a" opacity="0.45"/>'''
def svg(bg0,bg1,glow,ring,coat,hat,face,extra_front=''):
    defs,bod=coat
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>
<radialGradient id="bg" cx="50%" cy="46%" r="75%"><stop offset="0" stop-color="{bg0}"/><stop offset="1" stop-color="{bg1}"/></radialGradient>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff8dc"/><stop offset="0.5" stop-color="{glow}" stop-opacity="0.85"/><stop offset="0.8" stop-color="{glow}" stop-opacity="0.3"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<radialGradient id="skin" cx="42%" cy="38%" r="75%"><stop offset="0" stop-color="#ffe0bd"/><stop offset="1" stop-color="#f3bd8c"/></radialGradient>
{defs}<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter><clipPath id="frame"><rect width="1024" height="1024"/></clipPath></defs>
<g clip-path="url(#frame)" stroke-linejoin="round" stroke-linecap="round">
<rect width="1024" height="1024" fill="url(#bg)"/><circle cx="512" cy="455" r="420" fill="url(#glow)"/>
{ring}{bod}{HEAD}{hat}{face}{extra_front}</g></svg>'''

# ---------- 3. SECRET BOLT ----------
ring3 = glowstroke(hexa(512,470,392),'#4fe3d0',30) + f'''
<g transform="translate(818,180) rotate(30)"><path d="{hexa(0,0,52)}" fill="#4fe3d0" stroke="{INK}" stroke-width="14"/><circle r="22" fill="#0b2a33" stroke="{INK}" stroke-width="10"/></g>'''
cap3 = '''<path d="M 270 430 C 270 250 400 196 520 196 C 650 196 770 250 762 420 C 690 380 350 380 270 430 Z" fill="#59606e" stroke="#1b1522" stroke-width="24"/>
<path d="M 300 420 C 380 380 640 372 760 412 C 790 436 800 456 784 470 C 680 430 380 434 300 470 Z" fill="#3d434f" stroke="#1b1522" stroke-width="22"/>
<circle cx="520" cy="200" r="22" fill="#3d434f" stroke="#1b1522" stroke-width="14"/>'''
face3 = '''<path d="M 366 500 q 46 -14 92 0" fill="none" stroke="#1b1522" stroke-width="20"/><path d="M 566 500 q 46 -14 92 0" fill="none" stroke="#1b1522" stroke-width="20"/>
<circle cx="442" cy="528" r="22" fill="#1b1522"/><circle cx="642" cy="528" r="22" fill="#1b1522"/>
<path d="M 470 652 q 46 18 94 -6" fill="none" stroke="#1b1522" stroke-width="18"/>'''
hand3 = '''<rect x="487" y="604" width="50" height="150" rx="25" fill="url(#skin)" stroke="#1b1522" stroke-width="18"/>
<ellipse cx="512" cy="790" rx="78" ry="62" fill="url(#skin)" stroke="#1b1522" stroke-width="20"/>
<path d="M 470 778 q 40 18 84 0" fill="none" stroke="#1b1522" stroke-width="10" opacity="0.6"/>'''
coat3 = body('#3e8a8c','#245d63','''<path d="M 428 750 L 512 840 L 596 750" fill="#f6f0e2" stroke="#1b1522" stroke-width="20"/>''')
s3 = svg('#16465a','#06141f','#7ff2e2',ring3,coat3,cap3,face3,hand3)

# ---------- 4. CLEVER CLANK ----------
ring4 = glowstroke(gear(512,468,352,14,52),'#ff9f43',26) + f'''
<g transform="translate(800,236) rotate(18)"><path d="M -70 -40 L -30 -40 L -30 -10 L 30 -10 L 30 -40 L 70 -40 L 70 10 L 30 50 L -30 50 L -70 10 Z" fill="#ffd166" stroke="{INK}" stroke-width="14"/></g>
<g stroke="#fff3c4" stroke-width="16"><path d="M 742 150 l -20 -40"/><path d="M 806 136 l 6 -44"/><path d="M 866 156 l 30 -34"/></g>'''
hat4 = '''<path d="M 300 300 C 340 220 440 196 512 236 C 580 190 690 218 726 300 C 640 270 380 270 300 300 Z" fill="#3a2416" stroke="#1b1522" stroke-width="22"/>
<path d="M 278 404 C 360 360 664 360 746 404 L 746 446 C 664 404 360 404 278 446 Z" fill="#3a2a2a" stroke="#1b1522" stroke-width="18"/>
<circle cx="420" cy="392" r="62" fill="#9fe6ff" stroke="#1b1522" stroke-width="22"/><circle cx="604" cy="392" r="62" fill="#9fe6ff" stroke="#1b1522" stroke-width="22"/>
<path d="M 398 370 l 26 -16" stroke="#fff" stroke-width="14"/><path d="M 582 370 l 26 -16" stroke="#fff" stroke-width="14"/>
<rect x="472" y="380" width="80" height="24" rx="10" fill="#c9773a" stroke="#1b1522" stroke-width="12"/>'''
face4 = '''<path d="M 370 520 q 44 -40 88 0" fill="none" stroke="#1b1522" stroke-width="22"/><path d="M 566 520 q 44 -40 88 0" fill="none" stroke="#1b1522" stroke-width="22"/>
<path d="M 400 606 Q 512 680 624 606 Q 610 716 512 718 Q 414 716 400 606 Z" fill="#7a1f2b" stroke="#1b1522" stroke-width="20"/>
<path d="M 420 620 Q 512 670 604 620 L 598 646 Q 512 690 426 646 Z" fill="#fff"/>'''
coat4 = body('#3b6fd8','#24479a','''<path d="M 360 760 L 360 1024" stroke="#1b1522" stroke-width="40"/><path d="M 360 760 L 360 1024" stroke="#ffd166" stroke-width="20"/>
<path d="M 664 760 L 664 1024" stroke="#1b1522" stroke-width="40"/><path d="M 664 760 L 664 1024" stroke="#ffd166" stroke-width="20"/>
<rect x="430" y="860" width="164" height="110" rx="18" fill="#2f5bbf" stroke="#1b1522" stroke-width="16"/>''')
s4 = svg('#4a1d3a','#14060f','#ffb35c',ring4,coat4,hat4,face4)

# ---------- 6. THE CLEVER GAP ----------
R=362; ring6 = glowstroke(arc(512,468,R,-50,272),'#ffc94d',34) + glowstroke(arc(512,468,R,286,298),'#ffc94d',34)
ties=''
for a in range(-44,270,14):
    ra=math.radians(a); x0,y0=512+(R-34)*math.cos(ra),468+(R-34)*math.sin(ra); x1,y1=512+(R+34)*math.cos(ra),468+(R+34)*math.sin(ra)
    ties+=f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="#7a4a2c" stroke-width="16"/>'
ring6 = f'<g opacity="0.95">{ties}</g>' + ring6 + '<g stroke="#fff3c4" stroke-width="16"><path d="M 760 140 l 26 -46"/><path d="M 812 170 l 46 -22"/><path d="M 720 120 l 0 -50"/></g>'
hat6 = '''<path d="M 272 430 C 262 240 396 190 512 190 C 628 190 762 240 752 430 Z" fill="#2f4f9a" stroke="#1b1522" stroke-width="24"/>
<g stroke="#f6f0e2" stroke-width="16"><path d="M 360 214 L 330 420"/><path d="M 436 196 L 420 420"/><path d="M 512 192 L 512 420"/><path d="M 588 196 L 604 420"/><path d="M 664 214 L 694 420"/></g>
<path d="M 272 430 C 262 240 396 190 512 190 C 628 190 762 240 752 430 Z" fill="none" stroke="#1b1522" stroke-width="24"/>
<path d="M 250 430 C 350 400 674 400 774 430 C 800 450 790 480 760 476 C 660 452 364 452 264 476 C 234 480 226 450 250 430 Z" fill="#1f3570" stroke="#1b1522" stroke-width="22"/>'''
face6 = '''<path d="M 366 486 q 44 -34 88 -10" fill="none" stroke="#1b1522" stroke-width="20"/><path d="M 572 476 q 44 -24 88 10" fill="none" stroke="#1b1522" stroke-width="20"/>
<circle cx="414" cy="534" r="25" fill="#1b1522"/><circle cx="423" cy="525" r="8" fill="#fff"/><circle cx="614" cy="534" r="25" fill="#1b1522"/><circle cx="623" cy="525" r="8" fill="#fff"/>
<path d="M 430 628 Q 520 664 612 606 Q 596 704 512 706 Q 446 706 430 628 Z" fill="#7a1f2b" stroke="#1b1522" stroke-width="20"/>
<path d="M 449 640 Q 520 668 598 624 Q 594 644 588 656 Q 520 690 456 664 Z" fill="#fff"/>
<path d="M 520 300 q 0 0 0 0" />'''
coat6 = body('#2f8f5b','#1d6640','''<path d="M 428 750 L 512 868 L 596 750" fill="#f6f0e2" stroke="#1b1522" stroke-width="20"/>
<path d="M 494 760 L 530 760 L 522 880 L 502 880 Z" fill="#e2483d" stroke="#1b1522" stroke-width="10"/>
<circle cx="556" cy="930" r="17" fill="#ffc94d" stroke="#1b1522" stroke-width="10"/><circle cx="556" cy="1004" r="17" fill="#ffc94d" stroke="#1b1522" stroke-width="10"/>''')
s6 = svg('#1d3f9a','#081433','#ffe08a',ring6,coat6,hat6,face6)

for n,s in [('secret-bolt',s3),('clever-clank',s4),('the-clever-gap',s6)]: open(f'{n}.svg','w').write(s)
# lockups with name
font=base64.b64encode(open('/tmp/claude-0/-home-user-My-videos/887f0bcb-7a1d-5150-b8dc-8a87280c646f/scratchpad/build/fonts/Poppins-ExtraBold.ttf','rb').read()).decode()
open('font.b64','w').write(font)
