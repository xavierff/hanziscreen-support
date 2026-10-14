from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b'
ROOT=Path('/workspace/scratch/a80a755f3b22')
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def panda(d,x,y,r=40):
 for a in (-.7,.7):d.ellipse((x+a*r-r*.28,y-r-r*.15,x+a*r+r*.28,y-r+r*.4),fill=WHITE)
 d.ellipse((x-r,y-r,x+r,y+r),fill=WHITE)
 for a in (-.4,.4):
  d.ellipse((x+a*r-r*.22,y-r*.35,x+a*r+r*.22,y+r*.2),fill=BG)
  d.ellipse((x+a*r-r*.045,y-r*.12,x+a*r+r*.045,y-r*.03),fill=WHITE)
 d.ellipse((x-r*.12,y+r*.22,x+r*.12,y+r*.37),fill=BG)
 d.arc((x-r*.25,y+r*.28,x+r*.25,y+r*.65),0,180,fill=BG,width=2)
def shelves(d):
 d.rounded_rectangle((55,270,485,720),radius=25,outline=CYAN,width=6)
 for y in (420,570):d.line((55,y,485,y),fill=CYAN,width=5)
 for x in (195,345):d.line((x,270,x,720),fill=CYAN,width=3)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1248_panda_storage.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_2046/chat_pop_groove.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.8,afade=t=out:st=14.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','15',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(450):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<12:
  if t<3:
   text(d,'MY BRAIN LEARNS ONE',45,34,CYAN);text(d,'VERY IMPORTANT WORD',100,34)
   panda(d,270,460,105);text(d,'熊猫',620,64,YELLOW);text(d,'xióngmāo • PANDA',720,30)
  elif t<7:
   text(d,'BRAIN STORAGE',45,42,CYAN);text(d,'“We’ll make room.”',125,32,YELLOW)
   shelves(d)
   n=min(9,int((t-3)*3)+1)
   for j in range(n):
    x=125+(j%3)*145;y=350+(j//3)*150
    panda(d,x,y+5*math.sin(t*7+j),42)
   text(d,'熊猫  熊猫  熊猫',800,34,YELLOW)
  else:
   text(d,'WHAT’S MY WI-FI PASSWORD?',45,30,PINK);text(d,'BRAIN:',110,34,CYAN)
   shelves(d)
   for j in range(9):panda(d,125+(j%3)*145,350+(j//3)*150+5*math.sin(t*7+j),42)
   text(d,'“Best I can do is 熊猫.”',780,32,YELLOW);text(d,'Priorities.',845,42,WHITE)
 else:
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (45,135,195,285,405):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
