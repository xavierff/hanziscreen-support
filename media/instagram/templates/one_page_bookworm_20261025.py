from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,math,wave,numpy as np,hashlib,json
R=Path(__file__).parent;root=R.parent;W,H=1080,1920;fps=24;dur=20
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(R/'font.otf'),s) for s in range(24,121)}
def txt(d,s,y,size=60,c=WHITE):
 b=d.textbbox((0,0),s,font=F[size]);assert b[2]-b[0]<950,s;d.text(((1080-b[2]+b[0])/2,y),s,font=F[size],fill=c)
def animal(d,x,y,tiger=False,bob=0):
 y+=bob;c=YELLOW if tiger else PINK
 d.ellipse((x-100,y-90,x+100,y+100),fill=c)
 for dx in (-65,65):d.ellipse((x+dx-34,y-130,x+dx+34,y-60),fill=c)
 if not tiger:d.rounded_rectangle((x-70,y-55,x+70,y+150),radius=60,fill=c)
 for dx in (-34,34):d.ellipse((x+dx-9,y-15,x+dx+9,y+5),fill=BG)
 d.arc((x-35,y+30,x+35,y+65),0,180,fill=BG,width=6)
 if tiger:
  for dx in (-65,0,65):d.line((x+dx,y-75,x+dx*.8,y-35),fill=BG,width=13)
 d.rounded_rectangle((x-110,y+170,x+110,y+350),radius=35,fill=c)
 d.rectangle((x-135,y+220,x+135,y+320),fill=WHITE)
 d.text((x-110,y+233),'SO-SO',font=F[53],fill=BG)
widget=R/'widget.jpeg';assert hashlib.sha256(widget.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
wi=Image.open(widget).convert('RGB');wi.thumbnail((1080,1920),Image.Resampling.LANCZOS)
po=Image.open(R/'poster.jpeg').convert('RGB');po.thumbnail((960,1350),Image.Resampling.LANCZOS)
sr=44100;a=np.zeros(sr*dur)
def note(t,f,l=.3,v=.12):
 i=int(t*sr);u=np.arange(int(l*sr))/sr;n=min(len(u),len(a)-i);a[i:i+n]+=v*(np.sin(2*np.pi*f*u[:n])+.25*np.sin(2*np.pi*2*f*u[:n]))*np.exp(-u[:n]*12)
# Original One Page Waltz, synthesized without third-party samples.
for j,t in enumerate(np.arange(0,19.5,.34)):
 note(t,[293.66,369.99,440,587.33,493.88,440,369.99,220][j%8],.19,.08)
 if j%3==0:note(t,87.31,.18,.14)
for t in (0,.5,1,1.5,3,3.5,4,5.5,9,12,14,17):note(t,740,.12,.11)
a*=np.minimum(1,(dur-np.arange(len(a))/sr)/.5)
with wave.open(str(R/'audio.wav'),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-i',str(R/'audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(R/'2000_one_page_bookworm.mp4')],stdin=subprocess.PIPE)
frames=[]
for k in range(fps*dur):
 t=k/fps;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<9:
  txt(d,'POV: BECOMING A BOOKWORM',180,40,CYAN)
  if t<3:
   txt(d,'One page before bed.',300,65)
   txt(d,'My pillow: absolutely not.',410,55,YELLOW)
  elif t<6:
   txt(d,'The pillow can wait.',300,66)
   txt(d,'One sentence counts.',410,63,YELLOW)
  else:
   txt(d,'看书  kàn shū',300,83,CYAN)
   txt(d,'read a book / read books',430,53,YELLOW)
  # Original learner resists an impatient pillow and opens a real paper book.
  bob=math.sin(t*3)*8
  d.rounded_rectangle((180,1150,900,1400),radius=70,fill='#254a70')
  d.ellipse((400,680+bob,680,960+bob),fill='#75dfb0')
  for dx in (-43,43):d.ellipse((540+dx-9,815+bob,540+dx+9,835+bob),fill=BG)
  d.arc((495,850+bob,585,900+bob),0,180,fill=BG,width=7)
  d.rounded_rectangle((390,950,690,1240),radius=55,fill='#75dfb0')
  d.polygon([(315,1010),(540,1060),(765,1010),(765,1260),(540,1310),(315,1260)],fill=WHITE)
  d.line((540,1060,540,1300),fill=PINK,width=9)
  for j in range(4):
   yy=1090+j*44
   d.line((350,yy,495,yy+25),fill='#7693ac',width=6)
   d.line((585,yy+25,730,yy),fill='#7693ac',width=6)
  px=220+math.sin(t*4)*15 if t<3 else 180
  py=960 if t<3 else 1110
  d.rounded_rectangle((px-110,py-80,px+110,py+80),radius=40,fill=PINK)
  for dx in (-33,33):d.line((px+dx-10,py-5,px+dx+10,py-5),fill=BG,width=7)
  d.ellipse((px-10,py+20,px+10,py+43),fill=BG)
  txt(d,'A tiny reading habit.',1510,49)
 elif t<12:
  txt(d,'Follow for daily',550,76,CYAN);txt(d,'Mandarin memes',670,76,CYAN);txt(d,'& free Chinese lessons!',810,60,YELLOW)
 elif t<14:im.paste(wi,((W-wi.width)//2,(H-wi.height)//2))
 elif t<17:
  txt(d,'Hanzi on Screen',175,66);txt(d,'FREE TO START',275,64,YELLOW);im.paste(po,((W-po.width)//2,400))
 else:
  txt(d,'Useful Chinese.',370,80);txt(d,'On your iPhone.',480,76,CYAN);txt(d,'FREE TO START',700,72,YELLOW)
  txt(d,'Tap @hanziscreen',970,63);txt(d,'then the App Store link',1080,53);txt(d,'in our bio.',1170,63,YELLOW)
  txt(d,'TikTok: Search Hanzi Screen',1450,38);txt(d,'in the App Store',1510,38)
 if k in (12,84,156,240,312,372,444):frames.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
sheet=Image.new('RGB',(216*len(frames),384))
for i,f in enumerate(frames):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
f=R/'2000_one_page_bookworm.mp4';print(json.dumps({'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
