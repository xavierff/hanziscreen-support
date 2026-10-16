from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def desk(d,t):
 d.rounded_rectangle((40,650,500,672),radius=6,fill=CYAN)
 for x in (65,475):d.line((x,670,x,800),fill=CYAN,width=9)
 # Closed learning book remains closed throughout the fictional story.
 d.rounded_rectangle((170,555,330,645),radius=6,fill=YELLOW)
 d.line((183,560,183,640),fill=BG,width=3)
 d.text((208,568),'学习',font=F[36],fill=BG)
 d.line((200,624,315,624),fill=WHITE,width=5)
 if t>=3:
  # Lamp slides into the perfect position.
  shift=max(0,1-(t-3))*90
  d.line((105-shift,645,105-shift,480,155-shift,450),fill=PINK,width=8)
  d.polygon([(135-shift,425),(175-shift,425),(190-shift,465),(120-shift,465)],fill=PINK)
 if t>=4:
  x=430+max(0,1-(t-4))*110
  d.polygon([(x-27,595),(x+27,595),(x+20,645),(x-20,645)],fill=PINK)
  d.line((x,595,x,535),fill=CYAN,width=5)
  for dx,dy in [(-25,545),(23,558),(-18,568)]:d.ellipse((x+dx-13,dy-8,x+dx+13,dy+8),fill=CYAN)
 if t>=5:
  # Pencil is adjusted endlessly instead of opening the book.
  off=5*math.sin(t*5);d.line((355+off,620,395+off,570),fill=YELLOW,width=8)
  d.polygon([(393+off,568),(400+off,565),(397+off,577)],fill=WHITE)
def person(d,t):
 x=270;y=400+4*math.sin(t*3)
 d.ellipse((x-28,y-60,x+28,y-4),fill=CYAN)
 for dx in (-9,9):d.ellipse((x+dx-2,y-40,x+dx+2,y-34),fill=BG)
 d.line((x,y,x,y+145),fill=CYAN,width=9)
 d.line((x,y+35,x+75,y+90),fill=CYAN,width=8)
 d.line((x,y+35,x-75,y+90),fill=CYAN,width=8)
widget_path=ROOT/'run_20261015_noon/widget.jpeg';poster_path=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(widget_path.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(widget_path).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(poster_path).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2000_study_desk_designer.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1456/sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<10:
  person(d,t);desk(d,t)
  if t<3:
   txt(d,'POV: MY MANDARIN',40,37,CYAN);txt(d,'STUDY SETUP',98,43,YELLOW)
   txt(d,'“First, the perfect desk.”',220,31)
  elif t<7:
   txt(d,'LAMP. PLANT. PERFECT PENCIL.',40,27,PINK)
   txt(d,'Still arranging…',140,34)
  else:
   txt(d,'I BECAME AN',40,39,YELLOW);txt(d,'INTERIOR DESIGNER.',100,35,PINK)
   txt(d,'The book? Still closed.',220,32)
   # Sparkles celebrate the beautiful desk, not a learning outcome.
   for x,y in [(65,530),(470,475),(365,515)]:
    r=9+3*math.sin(t*5);d.line((x-r,y,x+r,y),fill=YELLOW,width=3);d.line((x,y-r,x,y+r),fill=YELLOW,width=3)
  txt(d,'学习 xuéxí • study / learn',850,28)
 elif t<12:
  txt(d,'GIVE CHINESE A PLACE',280,32,CYAN);txt(d,'ON YOUR LOCK SCREEN, TOO.',340,28,YELLOW)
  txt(d,'Genuine screenshot preview next',600,25)
 elif t<15:
  # Exact owner-requested CTA, split only for readability.
  txt(d,'Follow for daily',300,42,CYAN)
  txt(d,'Mandarin memes',365,42,CYAN)
  txt(d,'& free Chinese lessons!',440,34,YELLOW)
 elif t<17:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,170,260,400,475,555):frames.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(frames):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
