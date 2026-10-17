from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def person(d,x,y,c=CYAN):
 d.ellipse((x-28,y-65,x+28,y-9),fill=c)
 for dx in (-9,9):d.ellipse((x+dx-2,y-44,x+dx+2,y-38),fill=BG)
 d.line((x,y-9,x,y+85),fill=c,width=9)
 d.line((x-35,y+42,x,y+12,x+35,y+42),fill=c,width=8)
 for dx in (-30,30):d.line((x,y+85,x+dx,y+130),fill=c,width=8)
def dish(d,kind):
 d.pieslice((170,470,370,610),0,180,fill=CYAN)
 if kind==0:
  for i in range(5):d.arc((200+i*15,450,220+i*15,535),180,360,fill=YELLOW,width=4)
 elif kind==1:
  d.polygon([(185,540),(270,450),(355,540)],fill=WHITE)
 else:
  for x in (220,270,320):
   d.pieslice((x-24,488,x+24,543),180,360,fill=YELLOW)
   for dx in (-12,0,12):d.line((x+dx,496,x+dx+3,508),fill=BG,width=2)
wp=ROOT/'run_20261015_noon/widget.jpeg';pp=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(wp.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(wp).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(pp).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1200_anything_terms_apply.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(R/'carefree_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=18.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','19',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(570):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<3:
  txt(d,'“WHAT DO YOU WANT TO EAT?”',45,28,CYAN)
  txt(d,'随便',190,78,YELLOW);txt(d,'suíbiàn',305,34)
  txt(d,'“Anything is fine.”',375,36)
  person(d,155,600);person(d,385,600,PINK)
  txt(d,'Me, apparently being easygoing.',835,25)
 elif t<7:
  txt(d,'ALSO ME:',45,44,PINK)
  i=min(2,int((t-3)/1.25));txt(d,['NOODLES?','RICE?','DUMPLINGS?'][i],205,40)
  dish(d,i)
  # Fast visual veto stamp on each suggestion.
  q=min(1,((t-3)%1.25)/.25);w=int(150*q)
  if w>0:
   d.rounded_rectangle((270-w,650,270+w,745),radius=15,outline=PINK,width=5)
   if q>.75:txt(d,'NOPE.',655,50,PINK)
 elif t<11:
  txt(d,'随便*',40,65,YELLOW);txt(d,'*TERMS & CONDITIONS APPLY',145,25,PINK)
  # An exaggerated contract unrolls: the animation reveals the punchline.
  length=120+min(1,(t-7)/2)*430
  d.rounded_rectangle((100,290,440,290+length),radius=9,fill=WHITE)
  for i,s in enumerate(['NO NOODLES','NO RICE','NO DUMPLINGS','NOT TOO HOT','NOT TOO FAR','…IT’S A LONG LIST.']):
   yy=325+i*58
   if yy+30<290+length:
    b=d.textbbox((0,0),s,font=F[23]);d.text(((540-b[2])/2,yy),s,font=F[23],fill=BG)
  d.ellipse((90,270+length,450,315+length),fill=CYAN)
  txt(d,'“Anything” has a lot of rules.',875,27)
 elif t<14:
  txt(d,'Follow for daily',300,42,CYAN);txt(d,'Mandarin memes',365,42,CYAN)
  txt(d,'& free Chinese lessons!',440,34,YELLOW)
 elif t<16:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,160,290,370,450,530):frames.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(frames):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'audio_size':(R/'carefree_30s.mp3').stat().st_size}))
