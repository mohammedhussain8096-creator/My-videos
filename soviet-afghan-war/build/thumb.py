import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
W,H=1280,720
BANG="fonts/Bangers-Regular.ttf"; MARK="fonts/PermanentMarker.ttf"
def fit(p, fx=0.5, fy=0.5, z=1.0):
    im=Image.open(p).convert("RGB")
    im=ImageOps.fit(im,(int(W*z),int(H*z)),centering=(fx,fy))
    return im.resize((W,H),Image.LANCZOS) if z!=1 else im
def grade(im, warm=(1.15,0.95,0.8), con=1.35, sat=1.2, br=1.0):
    im=ImageEnhance.Contrast(im).enhance(con); im=ImageEnhance.Color(im).enhance(sat); im=ImageEnhance.Brightness(im).enhance(br)
    a=np.asarray(im).astype(np.float32)*np.array(warm); return Image.fromarray(a.clip(0,255).astype(np.uint8))
def vignette(im, s=0.55):
    yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    v=np.clip(1-s*np.clip(r-0.5,0,None)**1.5,0,1)[...,None]
    return Image.fromarray((np.asarray(im)*v).astype(np.uint8))
def text(d, xy, s, font, size, fill, stroke=10, anchor="la", shadow=None, base=None):
    f=ImageFont.truetype(font,size)
    if base is not None:
        sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((xy[0]+8,xy[1]+10),s,font=f,fill=(0,0,0,200),stroke_width=stroke,stroke_fill=(0,0,0,200),anchor=anchor)
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(base).text(xy,s,font=f,fill=fill,stroke_width=stroke,stroke_fill=(15,10,8),anchor=anchor)
    return f.getbbox(s,anchor=anchor,stroke_width=stroke)

# ---- A: Stinger painting
im=fit("img/first_sting.jpg",0.35,0.5); im=vignette(grade(im,(1.18,0.92,0.75),1.3,1.3)).convert("RGBA")
# dark gradient right side for text
g=np.zeros((H,W),np.float32); g[:]=np.clip((np.arange(W)-500)/600,0,1)*200
im.alpha_composite(Image.fromarray(np.dstack([np.zeros((H,W,3),np.uint8),g.astype(np.uint8)])))
text(None,(1240,150),"THE USSR'S",BANG,118,(255,255,255),9,"ra",base=im)
text(None,(1240,280),"VIETNAM",BANG,210,(255,212,30),12,"ra",base=im)
d=ImageDraw.Draw(im); pts=[(700+i*27,500+6*np.sin(i*.8)) for i in range(20)]
d.line(pts,fill=(255,255,255),width=22,joint="curve"); d.line(pts,fill=(205,25,25),width=12,joint="curve")
text(None,(1240,530),"1979 – 1989",MARK,64,(255,255,255),7,"ra",base=im)
im.convert("RGB").save("thumb/thumb_A.jpg",quality=95)

# ---- B: Hind helicopter + red sky
src=Image.open("img/hind_soviet.jpg").convert("RGB"); h=int(H*1.05); w=int(src.width*h/src.height)
src=src.resize((w,h),Image.LANCZOS)
bgc=tuple(int(x) for x in np.asarray(src)[5:40,5:40].reshape(-1,3).mean(0))
im=Image.new("RGB",(W,H),bgc)
m=np.clip(np.arange(w)/350,0,1)[None,:].repeat(h,0); m=np.minimum(m, np.clip((np.arange(h)[:,None]-20)/120,0,1)+0*m)
im.paste(src,(W-w+160,-20),Image.fromarray((m*255).astype(np.uint8)))
g=ImageOps.grayscale(im); a=np.asarray(g).astype(np.float32)/255
a=np.clip((a-0.5)*1.5+0.5,0,1)
col=np.dstack([a*255*1.0+ (1-a)*40, a*120+(1-a)*10, a*60+(1-a)*8])  # red/orange duotone
im=vignette(Image.fromarray(col.clip(0,255).astype(np.uint8)),0.7).convert("RGBA")
text(None,(60,70),"SUPERPOWER",BANG,150,(255,255,255),10,"la",base=im)
text(None,(60,215),"CRUSHED",BANG,230,(255,212,30),13,"la",base=im)
d=ImageDraw.Draw(im); pts=[(70+i*30,470+6*np.sin(i*.8)) for i in range(20)]
d.line(pts,fill=(255,255,255),width=22,joint="curve"); d.line(pts,fill=(205,25,25),width=12,joint="curve")
text(None,(70,500),"SOVIET-AFGHAN WAR",MARK,58,(255,255,255),7,"la",base=im)
im.convert("RGB").save("thumb/thumb_B.jpg",quality=95)
