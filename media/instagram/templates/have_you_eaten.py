from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
W,H,FPS,DUR=540,960,30,17
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b';ORANGE='#ffad5c'
FONT='/workspace/scratch/a80a755f3b22/run_0245/NotoSansCJKsc-Bold.otf'
POSTER='/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
AUDIO='/workspace/scratch/a80a755f3b22/run_1649/treehouse_breakbeat.wav'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,56,72)}
def center(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-(b[2]-b[0]))/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,color,mouth='smile',arms=False):
 d.ellipse((x-28,y-70,x+28,y-14),outline=color,width=5);d.ellipse((x-10,y-50,x-4,y-44),fill=WHITE);d.ellipse((x+7,y-50,x+13,y-44),fill=WHITE)
 if mouth=='o':d.ellipse((x-6,y-39,x+6,y-27),outline=color,width=3)
 elif mouth=='flat':d.line((x-11,y-32,x+11,y-32),fill=color,width=3)
 else:d.arc((x-12,y-42,x+12,y-24),0,180,fill=color,width=3)
 d.line((x,y-14,x,y+76),fill=color,width=7)
 if arms:d.line((x,y+10,x-55,y-25),fill=color,width=7);d.line((x,y+10,x+55,y-25),fill=color,width=7)
 else:d.line((x,y+10,x-38,y+38),fill=color,width=7);d.line((x,y+10,x+38,y+38),fill=color,width=7)
 d.line((x,y+76,x-28,y+125),fill=color,width=7);d.line((x,y+76,x+28,y+125),fill=color,width=7)
def bowl(d,x,y,color,kind='noodle'):
 d.arc((x-58,y-24,x+58,y+55),0,180,fill=color,width=6);d.line((x-58,y+15,x+58,y+15),fill=color,width=5)
 if kind=='noodle':
  for j in range(-36,37,18):d.arc((x+j-10,y-18,x+j+10,y+8),180,360,fill=YELLOW,width=3)
 elif kind=='rice':
  for j in range(-35,36,14):d.ellipse((x+j,y-8,x+j+9,y),fill=WHITE)
 else:
  for j in (-28,0,28):d.ellipse((x+j-12,y-14,x+j+12,y+8),fill=YELLOW)
poster=Image.open(POSTER).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'0051_have_you_eaten.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',AUDIO,'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.82,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<14:
  if t<3.2:
   center(d,'MY CHINESE FRIEND:',55,30,CYAN)
   d.rounded_rectangle((92,180,448,390),radius=30,fill=WHITE);center(d,'你吃了吗？',225,56,BG);center(d,'nǐ chī le ma?',310,30,CYAN)
   person(d,270,620,CYAN,mouth='smile',arms=True);center(d,'“Have you eaten?”',835,30,YELLOW)
  elif t<6.2:
   center(d,'ME, TAKING IT VERY SERIOUSLY:',55,30,CYAN)
   person(d,270,560,YELLOW,mouth='o',arms=True)
   for j in range(12):
    a=t*3+j*math.pi/6;r=125+18*(j%2);x=270+math.cos(a)*r;y=530+math.sin(a)*r
    d.ellipse((x-8,y-8,x+8,y+8),fill=[YELLOW,ORANGE,PINK][j%3])
   center(d,'DINNER EMERGENCY!',820,40,PINK)
  elif t<10.2:
   center(d,'I PREPARED FOR THIS MOMENT',45,34,YELLOW)
   # rolling banquet table
   prog=min(1,(t-6.2)/1.3);left=570-prog*535
   d.rectangle((left,620,left+470,655),fill=WHITE);d.line((left+50,655,left+35,780),fill=WHITE,width=8);d.line((left+420,655,left+435,780),fill=WHITE,width=8)
   bowl(d,left+95,585,ORANGE,'dumpling');bowl(d,left+235,585,CYAN,'noodle');bowl(d,left+375,585,GREEN,'rice')
   person(d,85,420,YELLOW,mouth='smile',arms=True)
   center(d,'Dumplings. Noodles. Rice.',825,30,WHITE)
  else:
   center(d,'FRIEND:',45,30,CYAN)
   d.rounded_rectangle((75,150,465,320),radius=28,fill=WHITE);center(d,'“It was just a greeting.”',205,30,BG)
   person(d,110,560,CYAN,mouth='flat');person(d,430,560,YELLOW,mouth='o')
   d.rectangle((75,745,465,765),fill=WHITE);bowl(d,170,710,ORANGE,'dumpling');bowl(d,270,710,CYAN,'noodle');bowl(d,370,710,GREEN,'rice')
   center(d,'So… we’re not eating?',835,30,PINK)
 else:
  center(d,'START LEARNING CHINESE',25,30);center(d,'FREE',70,46,YELLOW)
  im.paste(poster,((W-poster.width)//2,150));d=ImageDraw.Draw(im)
  center(d,'Try Hanzi on Screen FREE',858,30,YELLOW);center(d,'Link in bio',910,26)
 if k in (45,125,235,345,465):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
