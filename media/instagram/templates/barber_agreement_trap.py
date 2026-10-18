from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def haircut(d,t):
 # Original flat2D haircut gag; no actual testimonial or app UI.
 x=265;y=520
 d.rounded_rectangle((180,620,350,740),radius=16,outline=PINK,width=6)
 d.line((265,740,265,795),fill=PINK,width=7);d.line((215,795,315,795),fill=PINK,width=6)
 d.polygon([(225,565),(305,565),(345,685),(185,685)],fill=CYAN)
 d.ellipse((205,450,325,580),fill=CYAN)
 for xx in (244,286):d.ellipse((xx-4,505,xx+4,516),fill=BG)
 d.arc((247,535,284,555),0,180,fill=BG,width=3)
 hair=1 if t<4 else max(0,1-(t-4)/5)
 if hair>0:
  for i in range(9):
   xx=218+i*11;top=442-75*hair+10*math.sin(i)
   d.line((xx,475,xx-10,top),fill=YELLOW,width=max(4,int(16*hair)))
 # Scissors move across head, clipping away more hair with each pass.
 if 3<=t<9:
  xx=195+((t-3)*65)%155;yy=425-30*hair
  gap=10+8*abs(math.sin(t*13))
  for dy in (-gap,gap):d.ellipse((xx-22,yy+dy-8,xx-6,yy+dy+8),outline=PINK,width=3)
  d.line((xx-8,yy-gap,xx+38,yy+gap),fill=WHITE,width=4)
  d.line((xx-8,yy+gap,xx+38,yy-gap),fill=WHITE,width=4)
  for i in range(4):
   q=(t*.9+i*.21)%1;px=195+i*45
   d.line((px,560+q*150,px+12,570+q*150),fill=YELLOW,width=4)
 if t>=9:
  for xx,yy in [(235,473),(300,460)]:
   d.line((xx-8,yy,xx+8,yy),fill=WHITE,width=3);d.line((xx,yy-8,xx,yy+8),fill=WHITE,width=3)
wp=ROOT/'run_20261015_noon/widget.jpeg';pp=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(wp.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(wp).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(pp).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1200_barber_agreement_trap.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1456/sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=21.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','22',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(660):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<14:
  haircut(d,t)
  if t<3:
   txt(d,'MY MANDARIN AT THE BARBER:',40,27,CYAN)
   txt(d,'对！',145,72,YELLOW);txt(d,'duì • “Right!”',245,35)
   txt(d,'My most confident word.',850,29)
  elif t<9:
   txt(d,'“A BIT SHORTER?”',40,37,PINK)
   txt(d,'再短一点？',110,39);txt(d,'zài duǎn yìdiǎn?',174,27)
   txt(d,'对！',245,58,YELLOW)
   txt(d,'Me, continuing to agree…',850,29)
  else:
   txt(d,'NEXT LESSON:',35,35,PINK);txt(d,'可以了',100,58,YELLOW)
   txt(d,'kěyǐ le • “That’s enough.”',190,29)
   txt(d,'Learned this one a little late.',850,28)
 elif t<17:
  txt(d,'Follow for daily',300,42,CYAN);txt(d,'Mandarin memes',365,42,CYAN)
  txt(d,'& free Chinese lessons!',440,34,YELLOW)
 elif t<19:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (40,190,340,460,540,620):frames.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(frames):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
