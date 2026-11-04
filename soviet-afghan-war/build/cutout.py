import sys
from rembg import remove, new_session
from PIL import Image
sess=new_session(sys.argv[1])
for k in sys.argv[2:]:
    im=Image.open(f"img/{k}.jpg").convert("RGB")
    if im.width>1600: im=im.resize((1600,int(im.height*1600/im.width)))
    out=remove(im,session=sess,post_process_mask=True)
    out.save(f"cut/{k}.png"); print(k,flush=True)
