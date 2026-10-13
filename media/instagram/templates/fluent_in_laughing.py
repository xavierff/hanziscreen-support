from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib,wave,struct
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
W,H,FPS,DUR=540,960,30,17
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b'
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
POSTER='/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,56,72)}
def center(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-(b[2]-b[0]))/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,color,cap=False,arms=False):
 d.ellipse((x-28,y-70,x+28,y-14),outline=color,width=5)
 d.ellipse((x-10,y-50,x-4,y-44),fill=WHITE);d.ellipse((x+7,y-50,x+13,y-44),fill=WHITE)
 d.arc((x-13,y-42,x+13,y-24),0,180,fill=color,width=3)
 if cap:
  d.polygon([(x-55,y-73),(x,y-100),(x+55,y-73),(x,y-48)],fill=YELLOW)
  d.line((x+42,y-74,x+48,y-35),fill=YELLOW,width=4)
 d.line((x,y-14,x,y+75),fill=color,width=7)
 if arms:
  d.line((x,y+12,x-55,y-35),fill=color,width=7);d.line((x,y+12,x+55,y-35),fill=color,width=7)
 else:
  d.line((x,y+12,x-38,y+40),fill=color,width=7);d.line((x,y+12,x+38,y+40),fill=color,width=7)
 d.line((x,y+75,x-28,y+125),fill=color,width=7);d.line((x,y+75,x+28,y+125),fill=color,width=7)
def make_audio(path):
 sr=44100;s=[];notes=[523.25,659.25,783.99,1046.5]
 for i in range(sr*DUR):
  t=i/sr;step=int(t*5);q=(t*5)%1;n=notes[step%4]
  bell=(math.sin(2*math.pi*n*t)+.35*math.sin(2*math.pi*n*2.01*t))*math.exp(-11*q)
  popq=(t*2.5+.3)%1;pop=math.sin(2*math.pi*(180+300*popq)*t)*math.exp(-28*popq)
  bass=math.sin(2*math.pi*(n/4)*t)*math.exp(-15*q)
  fade=1 if t<16.2 else max(0,(17-t)/.8)
  v=(.21*bell+.12*pop+.10*bass)*fade;s.append(int(max(-1,min(1,v))*32767))
 with wave.open(str(path),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(struct.pack('<'+'h'*len(s),*s))
wav=R/'chat_pop_groove.wav';make_audio(wav)
poster=Image.open(POSTER).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2046_fluent_in_laughing.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(wav),'-vf','scale=1080:1920:flags=lanczos','-af','volume=.9','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<14:
  if t<3.2:
   center(d,'I JUST READ A WHOLE',60,34,CYAN);center(d,'CHINESE PARAGRAPH!',115,40,YELLOW)
   person(d,270,540,YELLOW,cap=True,arms=True)
   for j in range(22):
    a=j*.9+t*2;r=125+35*(j%3);x=270+math.cos(a)*r;y=520+math.sin(a)*r
    d.rectangle((x-4,y-4,x+4,y+4),fill=[PINK,CYAN,GREEN][j%3])
   center(d,'Basically fluent.',835,30)
  elif t<7.4:
   center(d,'THE “PARAGRAPH”:',55,30,CYAN)
   slide=max(0,1-(t-3.2)*2);x=35+slide*560
   d.rounded_rectangle((x,210,x+470,560),radius=36,fill=WHITE)
   rows=['哈哈哈哈','哈哈哈哈','哈哈哈哈']
   for j,row in enumerate(rows):
    d.text((x+55,250+j*90),row,font=fonts[56],fill=BG)
   person(d,110,710,YELLOW)
   # scanning checkmarks
   shown=min(3,int(max(0,t-4.0)*1.2))
   for j in range(shown):
    yy=285+j*90;d.line((475,yy,486,yy+12),fill=GREEN,width=6);d.line((486,yy+12,510,yy-18),fill=GREEN,width=6)
   center(d,'I KNOW EVERY CHARACTER!',855,30,YELLOW)
  elif t<10.5:
   center(d,'DICTIONARY:',70,30,CYAN)
   d.rounded_rectangle((65,205,475,640),radius=28,fill=WHITE)
   center(d,'哈哈',270,72,BG);center(d,'hāhā',380,40,CYAN);center(d,'“hahaha” / laughter',455,30,BG)
   for j in range(3):
    d.ellipse((145+j*110,560,205+j*110,620),fill=YELLOW)
    d.arc((160+j*110,580,190+j*110,605),0,180,fill=BG,width=4)
   center(d,'Oh.',790,46,PINK)
  else:
   center(d,'NEW LANGUAGE LEVEL:',65,30,CYAN);center(d,'FLUENT IN LAUGHING',120,40,YELLOW)
   person(d,270,540,YELLOW,cap=True,arms=True)
   d.rounded_rectangle((95,300,445,405),radius=25,fill=WHITE)
   center(d,'哈哈哈哈哈哈',325,46,BG)
   center(d,'Still counts.',830,34,GREEN)
  
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
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'audio_size':wav.stat().st_size,'audio_sha256':hashlib.sha256(wav.read_bytes()).hexdigest()}))
