from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b'
ROOT=Path('/workspace/scratch/a80a755f3b22')
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def eraser(d,x,y,scale=1):
 w=70*scale;h=36*scale
 d.rounded_rectangle((x-w,y-h,x+w,y+h),radius=10,fill=PINK,outline=WHITE,width=4)
 d.rectangle((x+15*scale,y-h+4,x+w-4,y+h-4),fill=CYAN)
 d.ellipse((x-30*scale,y-12*scale,x-24*scale,y-6*scale),fill=BG)
 d.ellipse((x-12*scale,y-12*scale,x-6*scale,y-6*scale),fill=BG)
 d.arc((x-31*scale,y-2*scale,x-4*scale,y+18*scale),0,180,fill=BG,width=3)
def pencil(d,x,y):
 d.polygon([(x,y),(x+20,y-85),(x+38,y-80),(x+15,y+5)],fill=YELLOW)
 d.polygon([(x,y),(x+15,y+5),(x-4,y+19)],fill=WHITE)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1044_eraser_wins.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1456/sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.78,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(510):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<14:
  if t<3:
   text(d,'CHINESE HANDWRITING:',45,34,CYAN);text(d,'ME vs. MY ERASER',105,38)
   d.rounded_rectangle((90,280,450,600),radius=20,fill=WHITE)
   text(d,'写',315,80,BG);text(d,'xiě • WRITE',465,32,BG)
   pencil(d,135,700);eraser(d,390,690)
   text(d,'Today, I master this character.',825,28,YELLOW)
  elif t<9:
   text(d,'ATTEMPTING THE FIRST STROKE…',45,28,CYAN)
   d.rounded_rectangle((75,245,465,700),radius=18,fill=WHITE)
   phase=(t-3)%2;progress=min(1,phase/.65)
   if phase<1.05:
    d.line((180,430,180+160*progress,430),fill=BG,width=10)
    pencil(d,180+160*progress,430)
   else:
    x=150+270*min(1,(phase-1.05)/.8)
    if x<350:d.line((max(180,x+50),430,350,430),fill=BG,width=10)
    eraser(d,x,430)
   text(d,['A little straighter…','Nope. Again.','Just one more try…'][min(2,int((t-3)/2))],810,32,PINK)
  else:
   text(d,'MY ERASER HAS STUDIED',45,32,CYAN);text(d,'MORE HANZI THAN I HAVE.',100,32,PINK)
   d.rounded_rectangle((75,245,465,700),radius=18,fill=WHITE)
   eraser(d,270,455,1.7+0.07*math.sin(t*6))
   for j in range(9):
    x=110+j*39;y=630+8*math.sin(j+t*3);d.ellipse((x,y,x+9,y+4),fill=PINK)
   text(d,'Paper: spotless.',795,34,GREEN);text(d,'Eraser: fluent.',850,38,YELLOW)
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
