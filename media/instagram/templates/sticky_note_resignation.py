from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);assert b[2]-b[0]<515,s
 d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=c)
def note(im,word,pinyin,x,y,angle=0):
 n=Image.new('RGBA',(122,122));d=ImageDraw.Draw(n)
 d.rounded_rectangle((1,1,120,120),radius=4,fill=YELLOW)
 for s,yy,sz in [(word,8,49),(pinyin,78,23)]:
  b=d.textbbox((0,0),s,font=fonts[sz]);d.text(((122-b[2]+b[0])/2,yy),s,font=fonts[sz],fill=BG)
 n=n.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 im.paste(n,(int(x-n.width/2),int(y-n.height/2)),n)
def room(d):
 # Original flat 2D room, not app UI.
 d.line((35,770,505,770),fill=WHITE,width=4)
 d.rounded_rectangle((80,330,270,767),radius=8,outline=CYAN,width=6)
 d.ellipse((240,550,250,560),fill=CYAN)
 d.rectangle((330,665,495,680),fill=PINK);d.line((345,680,345,770),fill=PINK,width=5);d.line((480,680,480,770),fill=PINK,width=5)
 d.rounded_rectangle((373,565,435,660),radius=10,outline=WHITE,width=5)
 d.arc((421,580,459,630),270,90,fill=WHITE,width=5)
def fan(d,t):
 x=65;y=610;d.ellipse((x-37,y-37,x+37,y+37),outline=PINK,width=4)
 for a in range(3):
  v=t*15+a*math.tau/3;d.line((x,y,x+28*math.cos(v),y+28*math.sin(v)),fill=PINK,width=8)
 d.line((x,y+40,x,y+100),fill=PINK,width=6);d.line((x-28,y+100,x+28,y+100),fill=PINK,width=5)
widget_path=ROOT/'run_20261015_noon/widget.jpeg';poster_path=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(widget_path.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
assert poster_path.stat().st_size==474864
widget=Image.open(widget_path).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(poster_path).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2000_sticky_note_resignation.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1456/sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=17.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','18',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(540):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<10:
  if t<3:
   txt(d,'POV: LABELING MY ROOM',45,30,CYAN);txt(d,'TO LEARN MANDARIN',100,32)
   txt(d,'Immersion. Nailed it.',210,31,YELLOW)
  elif t<7:
   txt(d,'THE FAN JOINS THE LESSON.',45,28,PINK)
  else:
   txt(d,'MY FLOOR IS FLUENT NOW.',45,30,YELLOW)
   txt(d,'I still need practice.',110,31)
  room(d)
  if t>=3:fan(d,t)
  q=max(0,min(1,(t-3)/3))
  note(im,'门','mén',178+q*145,475+q*310,math.sin(q*6)*30)
  note(im,'水','shuǐ',403-q*210,610+q*190,-math.sin(q*5)*35)
  if t>=3 and t<7:
   d=ImageDraw.Draw(im)
   for i in range(3):
    x=120+(t*100+i*75)%320;d.arc((x,580+i*30,x+65,600+i*30),180,350,fill=CYAN,width=2)
  if t>=7:txt(d,'门 mén • door   水 shuǐ • water',875,25)
 elif t<13:
  txt(d,'LESS PAPER.',220,46,PINK);txt(d,'MORE EVERYDAY CHINESE.',295,29,CYAN)
  txt(d,'See vocabulary on your',460,32);txt(d,'Lock Screen instead.',515,34,YELLOW)
  txt(d,'Genuine owner screenshot →',780,25)
 elif t<15:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,155,245,350,420,500):review.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(review):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
