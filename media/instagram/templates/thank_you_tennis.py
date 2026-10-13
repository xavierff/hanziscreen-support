from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;W,H,FPS,DUR=540,960,30,17
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65'
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,64)}
poster=Image.open('/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
def txt(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,color,swing=0,smile=False):
 d.ellipse((x-30,y-75,x+30,y-15),outline=color,width=5)
 for e in (x-10,x+10):d.ellipse((e-3,y-52,e+3,y-45),fill=WHITE)
 d.arc((x-13,y-41,x+13,y-27),0 if smile else 180,180 if smile else 360,fill=color,width=3)
 d.line((x,y-15,x,y+90),fill=color,width=7)
 d.line((x,y+90,x-28,y+142),fill=color,width=7);d.line((x,y+90,x+28,y+142),fill=color,width=7)
 d.line((x,y+15,x+40,y+30+swing),fill=color,width=7);d.line((x,y+15,x-25,y+35),fill=color,width=7)
 rx=x+45;ry=y-2+swing
 d.ellipse((rx-20,ry-30,rx+20,ry+30),outline=color,width=4);d.line((rx,ry+30,rx-5,ry+58),fill=color,width=5)
out=R/'1456_thank_you_tennis.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(R/'sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.7,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<14:
  if t<3:
   txt(d,'WHEN BOTH OF YOU',75,34);txt(d,'ONLY REMEMBER',128,34);txt(d,'"THANK YOU"',181,46,YELLOW)
  elif t<10:
   txt(d,'THE POLITENESS RALLY',78,34,CYAN)
  else:
   txt(d,'MATCH OVER.',78,46,YELLOW);txt(d,'WE FOUND "YOU ARE WELCOME".',145,26)
  phase=max(0,t-3);speed=1.0 if phase<3 else 1.7
  pos=(phase*speed)%2
  frac=pos if pos<1 else 2-pos
  swing=14*math.sin(t*9) if 3<t<10 else 0
  person(d,110,530,CYAN,swing,t>=10);person(d,395,530,YELLOW,-swing,t>=10)
  d.line((45,712,495,712),fill='#45658a',width=3)
  d.line((270,550,270,705),fill=WHITE,width=3)
  for j in range(7):d.line((260,555+j*21,280,555+j*21),fill='#45658a',width=2)
  if t<10:
   bx=158+frac*236;by=485-95*math.sin(frac*math.pi)
   d.ellipse((bx-11,by-11,bx+11,by+11),fill=YELLOW)
   if t>=3:
    label='谢谢!';lf=fonts[40];b=d.textbbox((0,0),label,font=lf)
    d.text((bx-b[2]/2,by-85),label,font=lf,fill=WHITE)
   txt(d,'谢谢  xièxie',785,40,CYAN);txt(d,'thank you',844,30)
  else:
   d.ellipse((258,688,278,708),fill=YELLOW)
   txt(d,'不客气  bù kèqi',340,40,CYAN)
   txt(d,'you are welcome',402,30)
   txt(d,'Finally. My arms were tired.',805,30,YELLOW)
 else:
  txt(d,'START LEARNING CHINESE',30,30);txt(d,'FREE',78,46,YELLOW)
  im.paste(poster,((W-poster.width)//2,158));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',865,30,YELLOW);txt(d,'Link in bio',916,26)
 if k in (30,180,345,465):review.append(im.resize((270,480)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
v=Image.new('RGB',(1080,480))
for i,f in enumerate(review):v.paste(f,(i*270,0))
v.save(R/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
