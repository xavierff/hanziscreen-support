from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=Path('/workspace/scratch/a80a755f3b22')
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,color=YELLOW,tired=False):
 d.ellipse((x-25,y-60,x+25,y-10),outline=color,width=5)
 for dx in (-8,8):d.ellipse((x+dx-2,y-40,x+dx+2,y-34),fill=WHITE)
 if tired:d.line((x-10,y-23,x+10,y-23),fill=WHITE,width=3)
 else:d.arc((x-12,y-32,x+12,y-14),0,180,fill=WHITE,width=3)
 d.line((x,y-10,x,y+60),fill=color,width=6);d.line((x,y+8,x-34,y+30),fill=color,width=6);d.line((x,y+8,x+34,y+30),fill=color,width=6)
 d.line((x,y+60,x-25,y+105),fill=color,width=6);d.line((x,y+60,x+25,y+105),fill=color,width=6)
def bag(d,x,y,label,color):
 d.rounded_rectangle((x-60,y-50,x+60,y+65),radius=15,fill=color)
 d.arc((x-20,y-70,x+20,y-30),180,360,fill=WHITE,width=5)
 b=d.textbbox((0,0),label,font=fonts[26]);d.text((x-(b[2]-b[0])/2,y-15),label,font=fonts[26],fill=BG)
 for dx in (-40,40):d.ellipse((x+dx-7,y+58,x+dx+7,y+72),fill=WHITE)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(ROOT/'upload/IMG_5435.jpeg').convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
out=R/'2045_verb_luggage.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1649/treehouse_breakbeat.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.8,afade=t=out:st=19.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<4:
  text(d,'ENGLISH VERB PACKING',45,34,CYAN);text(d,'FOR A TIME TRIP:',105,36)
  person(d,270,430,YELLOW,True)
  for j,label in enumerate(['EAT','ATE','EATEN']):
   q=max(0,min(1,(t-j*.7)/.6));bag(d,110+j*160,1000-350*q,label,[CYAN,PINK,YELLOW][j])
  text(d,'“I need OPTIONS.”',835,34,PINK)
 elif t<8:
  text(d,'MANDARIN VERB:',45,36,CYAN);text(d,'“I PACKED LIGHT.”',110,38,YELLOW)
  person(d,270,465,CYAN)
  d.polygon([(225,465),(250,445),(290,445),(315,465),(300,495),(290,480),(290,540),(250,540),(250,480),(240,495)],fill=WHITE)
  d.text((253,470),'吃',font=fonts[34],fill=BG)
  text(d,'吃 • chī • EAT',705,42,YELLOW);text(d,'Same verb form. Different time.',835,28)
 else:
  text(d,'EAT: THREE SUITCASES.',45,34,PINK);text(d,'吃: ONE OUTFIT.',105,40,CYAN)
  # tired English verb drags luggage past relaxed Mandarin verb
  x=80+min(1,(t-8)/5)*110;person(d,x,445,YELLOW,True)
  for j,label in enumerate(['EAT','ATE','EATEN']):bag(d,110+j*160,660+5*math.sin(t*4+j),label,[CYAN,PINK,YELLOW][j])
  person(d,425,445,CYAN);d.text((408,465),'吃',font=fonts[34],fill=WHITE)
  text(d,'“Same outfit, every timeline.”',815,30,YELLOW)
  text(d,'Chinese verbs do not conjugate for tense.',875,24)
 if t>=15 and t<17:im=Image.new('RGB',(540,960),BG);im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 elif t>=17:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (85,165,300,480,555):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
