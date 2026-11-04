import json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=3840,2160
C=json.load(open("geo/countries.geojson"))["features"]
R=json.load(open("geo/rivers.geojson"))["features"]
SEA=(196,212,222); LAND=(234,229,216); BORDER=(150,145,135); HL=(196,138,104); RIVER=(110,150,190)
def make(name, lon0, lon1, lat0, lat1, highlight=(), rivers=(), labels=(), pins=()):
    k=math.cos(math.radians((lat0+lat1)/2))
    sx=W/((lon1-lon0)*k); sy=H/(lat1-lat0); s=max(sx,sy)
    cx=(lon0+lon1)/2; cy=(lat0+lat1)/2
    P=lambda lo,la:(W/2+(lo-cx)*k*s, H/2-(la-cy)*s)
    im=Image.new("RGB",(W,H),SEA); d=ImageDraw.Draw(im)
    def polys(g):
        if g["type"]=="Polygon": return [g["coordinates"]]
        return g["coordinates"]
    for f in C:
        col=HL if f["properties"]["ADMIN"] in highlight else LAND
        for poly in polys(f["geometry"]):
            d.polygon([P(*p) for p in poly[0]],fill=col)
    for f in C:
        for poly in polys(f["geometry"]):
            d.line([P(*p) for p in poly[0]],fill=BORDER,width=4,joint="curve")
    for f in R:
        if f["properties"].get("name") in rivers:
            g=f["geometry"]; ls=[g["coordinates"]] if g["type"]=="LineString" else g["coordinates"]
            for l in ls: d.line([P(*p) for p in l],fill=RIVER,width=14,joint="curve")
    # paper texture
    import numpy as np
    a=np.asarray(im).astype(np.float32)
    rng=np.random.default_rng(1); n=rng.normal(0,1,(H//4,W//4)).astype(np.float32)
    n=np.asarray(Image.fromarray(((n*20)+128).clip(0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)-128
    a=(a+n[...,None]*0.5).clip(0,255)
    im=Image.fromarray(a.astype(np.uint8)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype("fonts/PermanentMarker.ttf",86)
    for (lo,la,txt) in labels:
        x,y=P(lo,la); d.text((x,y),txt,font=f,fill=(60,50,45),anchor="mm")
    meta={"pins":[{"x":P(lo,la)[0],"y":P(lo,la)[1],"label":t} for lo,la,t in pins]}
    im.save(f"maps/{name}.jpg",quality=92); json.dump(meta,open(f"maps/{name}.json","w"))
    print(name,meta)
make("amu",58,77,32,43,highlight=(),rivers=("Amu  Darya","Panj"),
     labels=[(64.0,40.6,"UZBEKISTAN"),(70.8,39.2,"TAJIKISTAN"),(66.5,34.6,"AFGHANISTAN")],
     pins=[(67.28,37.23,"AMU DARYA")])
make("kabul",50,84,24,44,highlight=("Afghanistan",),rivers=("Amu  Darya","Panj"),
     labels=[(65.3,33.2,"AFGHANISTAN"),(62.5,40.5,"USSR"),(70.0,28.0,"PAKISTAN"),(56.0,32.0,"IRAN")],
     pins=[(69.17,34.53,"KABUL")])
