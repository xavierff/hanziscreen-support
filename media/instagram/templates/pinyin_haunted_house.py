from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=Path('/workspace/scratch/a80a755f3b22')
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,scared=False):
 d.ellipse((x-25,y-60,x+25,y-10),outline=YELLOW,width=5)
 for dx in (-8,8):d.ellipse((x+dx-2,y-40,x+dx+2,y-34),fill=WHITE)
 if scared:d.ellipse((x-6,y-29,x+6,y-17),outline=WHITE,width=3)
 else:d.arc((x-12,y-32,x+12,y-14),0,180,fill=WHITE,width=3)
 d.line((x,y-10,x,y+60),fill=YELLOW,width=6)
 d.line((x,y+8,x-34,y+30),fill=YELLOW,width=6);d.line((x,y+8,x+34,y+30),fill=YELLOW,width=6)
 d.line((x,y+60,x-25,y+105),fill=YELLOW,width=6);d.line((x,y+60,x+25,y+105),fill=YELLOW,width=6)
def door(d,opened=False):
 d.rectangle((155,255,445,735),outline=CYAN,width=6)
 if opened:d.polygon([(165,260),(240,295),(240,700),(165,730)],fill='#244264',outline=WHITE)
 else:
  d.rectangle((163,263,437,727),fill='#244264');d.ellipse((400,485,413,498),fill=YELLOW)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(ROOT/'upload/IMG_5435.jpeg').convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
out=R/'1851_pinyin_haunted_house.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1456/sneaky_snitch.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.78,afade=t=out:st=22.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','23',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(690):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<4:
  text(d,'A HAUNTED HOUSE FOR',45,34,CYAN);text(d,'MANDARIN LEARNERS',100,38)
  door(d);d.text((190,350),'ENTER IF',font=fonts[28],fill=WHITE);d.text((190,400),'YOU DARE',font=fonts[28],fill=PINK)
  person(d,70+min(t,3)*25,680);text(d,'“Ghosts? I can handle ghosts.”',835,28,YELLOW)
 elif t<8:
  text(d,'THE DOOR OPENS…',45,36,PINK);door(d,True)
  text(d,'READ WITHOUT',110,34,WHITE);text(d,'PINYIN',160,46,YELLOW)
  # actual Hanzi on a classroom card, deliberately no pinyin
  d.rounded_rectangle((255,330,425,560),radius=16,fill=WHITE)
  d.text((272,360),'今天',font=fonts[52],fill=BG);d.text((272,440),'明天',font=fonts[52],fill=BG)
  person(d,115,675,True);text(d,'Not that kind of scary!',835,32,PINK)
 elif t<12:
  text(d,'ME:',45,34,CYAN);text(d,'“ABSOLUTELY NOT.”',100,38,PINK)
  door(d,True);person(d,115-(t-8)*90,675,True)
  for j in range(3):d.line((60,610+j*30,130,610+j*30),fill=YELLOW,width=4)
  text(d,'*leaves through the wall*',835,28,YELLOW)
 else:
  text(d,'PINYIN WAS MY',45,38,CYAN);text(d,'EMOTIONAL SUPPORT',105,34);text(d,'BLANKET.',160,46,PINK)
  person(d,270,450,True)
  d.rounded_rectangle((170,470,370,670),radius=30,fill=CYAN)
  d.text((220,530),'pīnyīn',font=fonts[28],fill=BG)
  text(d,'Ghosts: fine.',790,34);text(d,'No pinyin: nightmare.',845,32,YELLOW)
 if t>=18 and t<20:im=Image.new('RGB',(540,960),BG);im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 elif t>=20:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (50,180,305,435,565,650):review.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(review):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
