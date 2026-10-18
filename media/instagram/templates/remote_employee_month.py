from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def actor(d,x,y,c):
 d.ellipse((x-18,y-46,x+18,y-10),fill=c);d.line((x,y-10,x,y+65),fill=c,width=7)
 d.line((x-30,y+26,x,y+6,x+30,y+26),fill=c,width=6)
 for dx in (-23,23):d.line((x,y+65,x+dx,y+98),fill=c,width=6)
def remote(d,x,y,scale=1):
 w=38*scale;h=100*scale
 d.rounded_rectangle((x-w,y-h,x+w,y+h),radius=max(3,int(18*scale)),fill=CYAN)
 d.rounded_rectangle((x-24*scale,y-45*scale,x+24*scale,y+12*scale),radius=max(2,int(8*scale)),fill=BG)
 for dx in (-9,9):d.rectangle((x+(dx-3)*scale,y-32*scale,x+(dx+3)*scale,y-2*scale),fill=WHITE)
 for dx in (-15,15):d.ellipse((x+(dx-5)*scale,y+40*scale,x+(dx+5)*scale,y+50*scale),fill=BG)
wp=ROOT/'run_20261015_noon/widget.jpeg';pp=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(wp.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(wp).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(pp).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2000_remote_employee_month.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_20261017_noon/carefree_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<7:
  if t<3:
   txt(d,'POV: LEARNING MANDARIN',40,30,CYAN);txt(d,'THROUGH DRAMAS',98,35,YELLOW)
   txt(d,'“Just one episode.”',215,33)
  else:
   txt(d,'等一下！',40,63,YELLOW);txt(d,'děng yíxià • Wait a moment!',130,26)
  d.rounded_rectangle((50,325,490,640),radius=14,outline=WHITE,width=6)
  d.line((270,640,270,680),fill=WHITE,width=7);d.line((210,680,330,680),fill=WHITE,width=7)
  shift=12*math.sin(t*3) if t<3 else 0
  actor(d,185+shift,465,CYAN);actor(d,355-shift,465,PINK)
  # Original cartoon drama scene, not third-party footage.
  d.ellipse((247,385,267,407),fill=PINK);d.ellipse((265,385,285,407),fill=PINK);d.polygon([(247,399),(285,399),(266,422)],fill=PINK)
  if t>=3:
   for x in (257,277):d.rectangle((x,580,x+8,605),fill=WHITE)
  remote(d,390,800,.65)
  if t>=3:
   # A simple animated hand presses the physical remote's pause button.
   dx=7*math.sin(t*8);d.rounded_rectangle((400+dx,748,480,776),radius=10,fill=YELLOW)
  txt(d,'The pause button is doing overtime.',885,24)
 elif t<10:
  txt(d,'PAUSE BUTTON:',40,41,CYAN);txt(d,'EMPLOYEE OF THE MONTH',105,27,YELLOW)
  # Remote steps onto its own awards podium.
  y=550-10*math.sin((t-7)*3);remote(d,270,y,1.3)
  d.rounded_rectangle((170,690,370,765),radius=8,fill=YELLOW)
  d.ellipse((244,y+45,296,y+97),fill=YELLOW);d.polygon([(250,y+83),(252,y+127),(270,y+113),(288,y+127),(290,y+83)],fill=PINK)
  txt(d,'My remote deserves the credit.',850,28)
 elif t<12:
  txt(d,'KEEP EVERYDAY CHINESE',260,31,CYAN);txt(d,'IN SIGHT.',320,46,YELLOW)
  txt(d,'On your Lock Screen.',470,35)
  txt(d,'Genuine screenshot preview next',710,24)
 elif t<15:
  txt(d,'Follow for daily',300,42,CYAN);txt(d,'Mandarin memes',365,42,CYAN)
  txt(d,'& free Chinese lessons!',440,34,YELLOW)
 elif t<17:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,160,260,400,475,555):frames.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(frames):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
