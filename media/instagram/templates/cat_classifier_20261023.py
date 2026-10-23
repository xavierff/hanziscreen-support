from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,math,wave,numpy as np,hashlib,json
R=Path(__file__).parent;root=R.parent;W,H=1080,1920;fps=24;dur=20
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
F={s:ImageFont.truetype(str(root/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(24,121)}
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
widget=root/'run_20261015_noon/widget.jpeg';assert hashlib.sha256(widget.read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
wi=Image.open(widget).convert('RGB');wi.thumbnail((1080,1920),Image.Resampling.LANCZOS)
po=Image.open(root/'run_20261015_noon/poster.jpeg').convert('RGB');po.thumbnail((960,1350),Image.Resampling.LANCZOS)
sr=44100;a=np.zeros(sr*dur)
def note(t,f,l=.3,v=.12):
 i=int(t*sr);u=np.arange(int(l*sr))/sr;n=min(len(u),len(a)-i);a[i:i+n]+=v*(np.sin(2*np.pi*f*u[:n])+.25*np.sin(2*np.pi*2*f*u[:n]))*np.exp(-u[:n]*12)
# Original Cat Counter Pizzicato; deterministic synthesis, no recordings.
for j,t in enumerate(np.arange(0,19.5,.29)):
 note(t,[392,493.88,587.33,493.88,349.23,440,523.25,440][j%8],.16,.075)
 if j%4==0:note(t,98,.18,.13)
for t in (0,.6,2.7,4,5.5,9,12,14,17):note(t,1174.66,.14,.11)
a*=np.minimum(1,(dur-np.arange(len(a))/sr)/.5)
with wave.open(str(R/'audio.wav'),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-i',str(R/'audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(R/'1200_cat_classifier.mp4')],stdin=subprocess.PIPE)
frames=[]
for k in range(fps*dur):
 t=k/fps;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<9:
  txt(d,'MANDARIN LEARNER PROBLEMS',185,37,CYAN)
  def cat(x,y,angry=False):
   d.ellipse((x-140,y-100,x+140,y+180),fill=YELLOW)
   d.polygon([(x-130,y-15),(x-140,y-200),(x-25,y-80)],fill=YELLOW)
   d.polygon([(x+130,y-15),(x+140,y-200),(x+25,y-80)],fill=YELLOW)
   for dx in (-57,57):
    if angry:d.line((x+dx-24,y+5,x+dx+24,y+5),fill=BG,width=10)
    else:d.ellipse((x+dx-10,y-10,x+dx+10,y+20),fill=BG)
   d.polygon([(x-15,y+45),(x+15,y+45),(x,y+62)],fill=PINK)
   d.arc((x-30,y+64,x+30,y+100),0,180,fill=BG,width=7)
   for side in (-1,1):
    for dy in (-10,25):d.line((x+side*90,y+60+dy,x+side*190,y+45+dy),fill=WHITE,width=5)
  if t<2.7:
   txt(d,'I learned to count in Chinese.',310,54)
   txt(d,'My cat hired a grammar lawyer.',420,49,YELLOW)
   cat(540+math.sin(t*4)*18,1010,True)
   txt(d,'“You forgot my classifier.”',1510,53)
  elif t<5.5:
   txt(d,'THE CAT’S TERMS:',310,68)
   txt(d,'“I require 只.”',430,80,YELLOW)
   cat(540,1000,True)
   d.rounded_rectangle((340,1300,740,1470),radius=20,fill=CYAN)
   d.text((405,1310),'只 zhī',font=F[85],fill=BG)
  else:
   txt(d,'一只猫 • yì zhī māo',310,69,YELLOW)
   txt(d,'one cat',425,73)
   cat(540,1000+math.sin(t*6)*12)
   txt(d,'Permission to count: granted.',1500,46)
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
f=R/'1200_cat_classifier.mp4';print(json.dumps({'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
