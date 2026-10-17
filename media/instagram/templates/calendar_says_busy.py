from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=R.parent
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<510,s
 d.text(((540-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def label(d,s,x,y,size=24,c=BG):
 b=d.textbbox((0,0),s,font=F[size]);d.text((x-b[2]/2,y),s,font=F[size],fill=c)
def calendar(d,t):
 shake=5*math.sin(t*25) if 3<=t<7 else 0
 d.rounded_rectangle((60+shake,400,480+shake,760),radius=14,outline=WHITE,width=5)
 d.rectangle((62+shake,402,478+shake,460),fill=WHITE);label(d,'MY DAY',270+shake,409,28)
 for x,y,w,h,s,c in [(78,482,180,105,'WORK',CYAN),(278,482,180,105,'CHORES',PINK),(78,607,180,130,'ERRANDS',PINK),(278,607,180,130,'SLEEP',CYAN)]:
  d.rounded_rectangle((x+shake,y,x+w+shake,y+h),radius=8,fill=c);label(d,s,x+w/2+shake,y+30,23)
def block(im,x,y,angle=0):
 a=Image.new('RGBA',(320,110));d=ImageDraw.Draw(a);d.rounded_rectangle((2,2,318,108),radius=12,fill=YELLOW)
 label(d,'LEARN MANDARIN',160,31,28)
 a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);im.paste(a,(int(x-a.width/2),int(y-a.height/2)),a)
wp=ROOT/'run_20261015_noon/widget.jpeg';pp=ROOT/'run_20261015_noon/poster.jpeg'
assert hashlib.sha256(wp.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget=Image.open(wp).convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
poster=Image.open(pp).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2000_calendar_says_busy.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1646/fluffing_a_duck_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.65,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
frames=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<10:
  calendar(d,t)
  if t<3:
   txt(d,'POV: FITTING MANDARIN',40,32,CYAN);txt(d,'INTO MY DAY',100,41,YELLOW)
   block(im,270,285)
   txt(d,'“There must be room somewhere.”',850,25)
  elif t<7:
   txt(d,'JUST… SQUEEZE… IT… IN…',45,31,PINK)
   y=330+35*abs(math.sin((t-3)*4));block(im,270,y)
   d=ImageDraw.Draw(im);d.line((270,215,270,265),fill=PINK,width=8)
   d.polygon([(250,249),(290,249),(270,275)],fill=PINK)
   txt(d,'My calendar starts fighting back.',850,25)
  else:
   txt(d,'EVEN MY CALENDAR SAYS:',35,30,PINK)
   txt(d,'太忙了',110,57,YELLOW);txt(d,'tài máng le • too busy!',194,28)
   # The calendar ejects the oversized study block with a cartoon bounce.
   q=min(1,(t-7)/1.5);block(im,270+q*360,345-q*180,q*65)
   d=ImageDraw.Draw(im)
   txt(d,'INVITATION DECLINED.',830,32,PINK)
 elif t<12:
  txt(d,'A LITTLE CHINESE.',250,39,CYAN)
  txt(d,'SOMEWHERE YOU ALREADY LOOK.',325,25)
  txt(d,'Your Lock Screen.',450,40,YELLOW)
  txt(d,'Genuine screenshot preview next',700,24)
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
