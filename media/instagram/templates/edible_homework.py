from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b'
FONT='/workspace/scratch/a80a755f3b22/run_0245/NotoSansCJKsc-Bold.otf'
POSTER='/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
AUDIO='/workspace/scratch/a80a755f3b22/run_1649/treehouse_breakbeat.wav'
fonts={s:ImageFont.truetype(FONT,s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def dumpling(d,x,y,scale=1):
 a=38*scale;b=23*scale
 d.pieslice((x-a,y-b,x+a,y+b),180,360,fill=YELLOW,outline=WHITE,width=3)
 for j in range(-2,3):d.line((x+j*10*scale,y-b*.75,x+j*12*scale,y-3*scale),fill=BG,width=2)
 d.line((x-a,y,x+a,y),fill=WHITE,width=3)
def face(d,t,hungry=False):
 x=270;y=420
 d.ellipse((x-75,y-75,x+75,y+75),outline=CYAN,width=7)
 d.ellipse((x-35,y-25,x-23,y-13),fill=WHITE);d.ellipse((x+23,y-25,x+35,y-13),fill=WHITE)
 if hungry:d.ellipse((x-28,y+10,x+28,y+53),fill=BG,outline=WHITE,width=4)
 else:d.arc((x-30,y,x+30,y+46),0,180,fill=WHITE,width=5)
 d.line((270,497,270,565),fill=CYAN,width=7)
poster=Image.open(POSTER).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'0845_edible_homework.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',AUDIO,'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.82,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(510):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<14:
  d.ellipse((55,575,485,775),fill='#163459',outline=WHITE,width=6)
  if t<3:
   text(d,'MANDARIN HOMEWORK:',45,34,CYAN);text(d,'COUNT 10 DUMPLINGS',100,34)
   face(d,t);text(d,'Finally. A lesson I can taste.',820,28,PINK)
   for j in range(10):dumpling(d,110+(j%5)*80,650+(j//5)*65)
  elif t<9:
   n=min(3,int((t-3)/2)+1);phase=((t-3)%2)/2
   text(d,['一','二','三'][n-1],50,80,YELLOW);text(d,['yī • ONE','èr • TWO','sān • THREE'][n-1],155,36,CYAN)
   face(d,t,True)
   # each spoken count is followed by a dumpling flying into the mouth
   eaten=n-1
   for j in range(eaten+1,10):dumpling(d,110+(j%5)*80,650+(j//5)*65)
   x0=110+(eaten%5)*80;y0=650+(eaten//5)*65
   q=min(1,phase*1.4);dumpling(d,x0+(270-x0)*q,y0+(460-y0)*q,max(.2,1-q*.7))
   text(d,'Count. Bite. Repeat.',820,32,PINK)
  else:
   text(d,'WAIT… WHERE IS MY',45,34);text(d,'HOMEWORK?',100,54,PINK)
   face(d,t);text(d,'Counted to three.',790,32,CYAN);text(d,'Ate all ten.',845,42,YELLOW)
   # empty plate and a satisfied learner: the visual punchline
   d.arc((230,470,310,520),0,180,fill=YELLOW,width=6)
 else:
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (45,135,220,350,465):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
