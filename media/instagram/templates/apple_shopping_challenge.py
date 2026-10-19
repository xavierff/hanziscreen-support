from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def apple(d,x,y,r=25):
 d.ellipse((x-r,y-r,x+5,y+r),fill=PINK);d.ellipse((x-5,y-r,x+r,y+r),fill=PINK)
 d.line((x,y-r,x+4,y-r-12),fill=YELLOW,width=4)
 d.ellipse((x+4,y-r-15,x+20,y-r-5),fill=CYAN)
def person(d,x,y):
 d.ellipse((x-22,y-55,x+22,y-11),fill=CYAN)
 for dx in (-7,7):d.ellipse((x+dx-2,y-39,x+dx+2,y-33),fill=BG)
 d.line((x,y-11,x,y+70),fill=CYAN,width=8)
 d.line((x,y+12,x+45,y+35),fill=CYAN,width=7)
 for dx in (-25,25):d.line((x,y+70,x+dx,y+110),fill=CYAN,width=7)
def cart(d,x,y):
 d.line((x-95,y-80,x-75,y+30,x+100,y+30,x+115,y-65,x-90,y-65),fill=WHITE,width=5)
 d.line((x-95,y-80,x-125,y-85),fill=WHITE,width=5)
 for dx in (-52,65):d.ellipse((x+dx-12,y+45,x+dx+12,y+69),fill=CYAN)
wp=ROOT/'run_20261015_noon/widget.jpeg';pp=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(wp.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(wp).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(pp).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1200_apple_shopping_challenge.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(R/'investigations_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<3:
  txt(d,'MANDARIN SHOPPING CHALLENGE',35,26,CYAN)
  txt(d,'ONLY BUY WHAT',150,40,YELLOW);txt(d,'YOU CAN NAME.',210,40,YELLOW)
  person(d,140,525);cart(d,330,600)
  txt(d,'Me: “Easy.”',835,34)
 elif t<7:
  txt(d,'苹果',40,74,YELLOW);txt(d,'píngguǒ • apple',145,34)
  person(d,110,525);cart(d,315,620)
  for i in range(min(9,1+int((t-3)*2))):
   x=255+(i%3)*58;y=605-(i//3)*48;apple(d,x,y,25)
  # One more apple falls into the cart on the musical pulse.
  q=(t-3)%1;apple(d,360,350+q*150,24)
  txt(d,'My strongest grocery vocabulary.',835,25)
 elif t<12:
  txt(d,'I ACCIDENTALLY OPENED',35,30,CYAN);txt(d,'AN APPLE SHOP.',95,39,PINK)
  # The cart becomes a tiny fruit stall: a new outcome, not a learning guarantee.
  d.rectangle((75,360,465,690),outline=WHITE,width=5)
  for i in range(6):d.rectangle((75+i*65,325,140+i*65,395),fill=PINK if i%2==0 else YELLOW)
  for j in range(3):
   for i in range(5):apple(d,125+i*72,490+j*58,25)
  d.rectangle((75,690,465,745),fill=CYAN)
  d.text((125,697),'苹果 • APPLES',font=F[31],fill=BG)
  txt(d,'Next lesson: literally any vegetable.',830,25,YELLOW)
 elif t<15:
  txt(d,'Follow for daily',300,42,CYAN);txt(d,'Mandarin memes',365,42,CYAN)
  txt(d,'& free Chinese lessons!',440,34,YELLOW)
 elif t<17:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,170,290,400,475,555):frames.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(frames):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'audio_size':(R/'investigations_30s.mp3').stat().st_size}))
