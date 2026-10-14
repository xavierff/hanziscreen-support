from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=Path('/workspace/scratch/a80a755f3b22')
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def person(d,x,y):
 d.ellipse((x-22,y-55,x+22,y-11),outline=CYAN,width=5)
 d.line((x,y-11,x,y+50),fill=CYAN,width=6);d.line((x,y+5,x-30,y+30),fill=CYAN,width=6);d.line((x,y+5,x+30,y+30),fill=CYAN,width=6)
 d.line((x,y+50,x-22,y+90),fill=CYAN,width=6);d.line((x,y+50,x+22,y+90),fill=CYAN,width=6)
 for dx in (-7,7):d.ellipse((x+dx-2,y-37,x+dx+2,y-31),fill=WHITE)
def dog(d,x,y,s=1):
 # friendly flat 2D puppy, scaled up for the visual punchline
 d.rounded_rectangle((x-55*s,y-40*s,x+45*s,y+22*s),radius=int(18*s),fill=YELLOW)
 d.ellipse((x+20*s,y-65*s,x+80*s,y-5*s),fill=YELLOW)
 d.ellipse((x+15*s,y-62*s,x+38*s,y-15*s),fill=PINK)
 d.ellipse((x+60*s,y-42*s,x+66*s,y-36*s),fill=BG)
 d.ellipse((x+73*s,y-29*s,x+83*s,y-20*s),fill=BG)
 for dx in (-35,25):d.rounded_rectangle((x+dx*s,y+10*s,x+(dx+13)*s,y+48*s),radius=max(2,int(5*s)),fill=YELLOW)
 d.line((x-48*s,y-15*s,x-78*s,y-45*s),fill=YELLOW,width=max(3,int(12*s)))
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(ROOT/'upload/IMG_5435.jpeg').convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
out=R/'2251_little_dog_big_dog.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_2046/chat_pop_groove.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.8,afade=t=out:st=19.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<4:
  text(d,'NAMING MY PUPPY',45,38,CYAN);text(d,'WITH MY TINY MANDARIN:',105,29)
  text(d,'小狗',240,78,YELLOW);text(d,'xiǎogǒu • LITTLE DOG / PUPPY',350,25)
  person(d,140,570);dog(d,350,625,.8)
  text(d,'“Perfect. That’s his nickname.”',830,28,PINK)
 elif t<9:
  text(d,'A FEW MONTHS LATER…',45,34,CYAN)
  grow=.8+min(1,(t-4)/3.5)*2.1
  person(d,80,625);dog(d,285,580,grow)
  d.rounded_rectangle((150,760,420,840),radius=20,outline=PINK,width=4)
  text(d,'Nickname: 小狗',775,30,YELLOW)
 else:
  text(d,'THE DOG GREW.',45,42,YELLOW);text(d,'MY VOCABULARY DIDN’T.',110,28,PINK)
  # dog now takes the owner for a walk
  shift=15*math.sin(t*2);dog(d,280+shift,555,2.8)
  person(d,75+shift,690);d.line((105+shift,700,300+shift,560),fill=WHITE,width=4)
  text(d,'Still calling him “Little Dog.”',835,29,WHITE)
 if t>=15 and t<17:im=Image.new('RGB',(540,960),BG);im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 elif t>=17:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (60,205,355,480,555):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
