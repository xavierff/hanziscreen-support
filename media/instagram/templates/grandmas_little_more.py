from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<515,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def person(d,x,y,color=CYAN,grandma=False,scale=1):
 def pt(a,b):return (x+a*scale,y+b*scale)
 d.ellipse((*pt(-25,-65),*pt(25,-15)),fill=color)
 if grandma:
  d.ellipse((*pt(-10,-84),*pt(15,-60)),fill=WHITE)
  for xx in (-12,12):d.ellipse((*pt(xx-9,-50),*pt(xx+9,-32)),outline=BG,width=2)
  d.line((*pt(-3,-42),*pt(3,-42)),fill=BG,width=2)
 else:
  for xx in (-9,9):d.ellipse((*pt(xx-2,-46),*pt(xx+2,-39)),fill=BG)
 d.line((*pt(0,-15),*pt(0,70)),fill=color,width=max(3,int(8*scale)))
 for xx in (-30,30):d.line((*pt(0,70),*pt(xx,110)),fill=color,width=max(3,int(8*scale)))
 d.line((*pt(-35,30),*pt(0,5),*pt(35,30)),fill=color,width=max(3,int(7*scale)))
def bowl(d,cx,cy,w):
 d.pieslice((cx-w,cy-w*.30,cx+w,cy+w*.30),0,180,fill=PINK)
 d.line((cx-w,cy,cx+w,cy),fill=WHITE,width=4)
widget_path=ROOT/'run_20261015_noon/widget.jpeg';poster_path=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(widget_path.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(widget_path).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(poster_path).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1200_grandmas_little_more.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1646/fluffing_a_duck_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<3:
  txt(d,'MANDARIN AT GRANDMA’S',40,31,CYAN)
  txt(d,'我饱了',160,60,YELLOW);txt(d,'wǒ bǎo le',245,30);txt(d,'“I’m full.”',295,35)
  person(d,160,585);person(d,400,585,PINK,True)
  bowl(d,260,660,55);txt(d,'Dinner: completed.',825,30)
 elif t<7:
  txt(d,'GRANDMA:',40,33,PINK);txt(d,'再吃一点',140,60,YELLOW)
  txt(d,'zài chī yìdiǎn',225,31);txt(d,'“Eat a little more.”',285,34)
  person(d,150,585);person(d,410,585,PINK,True)
  d.line((375,615,300,550),fill=PINK,width=8)
  d.ellipse((270,530,320,555),fill=WHITE)
  drop=(t-3)%1
  d.ellipse((285,550+drop*90,301,562+drop*90),fill=WHITE)
  bowl(d,260,665,65)
  txt(d,'A little. Obviously.',825,30)
 elif t<15:
  txt(d,'GRANDMA’S “A LITTLE”:',40,32,YELLOW)
  # A rising pile transforms dinner into a mountain; tiny learner has to climb it.
  q=min(1,(t-7)/1.5);peak=620-q*275
  d.polygon([(55,735),(265,peak),(485,735)],fill=WHITE)
  d.polygon([(265,peak),(300,735),(485,735)],fill='#c2d5e2')
  for i in range(22):
   yy=peak+45+(735-peak-80)*(i%6)/6;xx=265+(i%2*2-1)*(yy-peak)*.38
   d.line((xx-4,yy,xx+3,yy-3),fill='#96afc2',width=2)
  bowl(d,270,735,225)
  climb=min(1,max(0,(t-8)/2.5));x=95+climb*165;y=690-climb*(690-peak+10)
  person(d,x,y,CYAN,False,.45)
  if t>=10.5:
   d.line((270,peak-10,270,peak-82),fill=CYAN,width=3)
   d.polygon([(270,peak-82),(338,peak-65),(270,peak-45)],fill=PINK)
  txt(d,'My dinner has a summit.',825,32,PINK)
  if t>=11:txt(d,'Follow for Mandarin Mini Moments',890,23,CYAN)
 if 15<=t<17:
  im=Image.new('RGB',(540,960),BG);im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 elif t>=17:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,145,350,475,555):frames.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(frames):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
