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
# Original Pocket Patrol, synthesized without third-party samples.
for j,t in enumerate(np.arange(0,19.5,.31)):
 note(t,[220,277.18,329.63,440,369.99,329.63,277.18,164.81][j%8],.19,.08)
 if j%3==0:note(t,82.41,.18,.14)
for t in (0,.5,1,1.5,3,3.5,4,5.5,9,12,14,17):note(t,740,.12,.11)
a*=np.minimum(1,(dur-np.arange(len(a))/sr)/.5)
with wave.open(str(R/'audio.wav'),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-i',str(R/'audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(R/'2000_pocket_phone_rescue.mp4')],stdin=subprocess.PIPE)
frames=[]
for k in range(fps*dur):
 t=k/fps;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<9:
  txt(d,'POV: LAUNDRY DAY',180,44,CYAN)
  if t<3:
   txt(d,'My phone joined the laundry.',300,55)
   txt(d,'It did not pack a swimsuit.',410,58,YELLOW)
  elif t<6:
   txt(d,'Pocket check. Phone rescued.',300,54)
   txt(d,'The sock is still missing.',410,59,YELLOW)
  else:
   txt(d,'口袋 kǒudài = pocket',300,66,CYAN)
   txt(d,'手机 shǒujī = mobile phone',420,53,YELLOW)
  # Cartoon laundry basket, shirt with pocket and escaping phone.
  d.rounded_rectangle((180,1050,900,1390),radius=40,fill='#266189',outline=CYAN,width=12)
  for xx in range(230,870,100):d.line((xx,1110,xx,1330),fill=CYAN,width=9)
  d.polygon([(380,750),(275,820),(200,1010),(330,1070),(375,970),(375,1200),(715,1200),(715,970),(760,1070),(890,1010),(815,820),(700,750)],fill=PINK)
  d.arc((460,690,620,825),0,180,fill=BG,width=20)
  d.rounded_rectangle((570,900,680,1060),radius=13,outline=WHITE,width=8)
  lift=0 if t<2 else min((t-2)/1.8,1)*300
  px=625+math.sin(t*9)*9 if t<3 else 625
  py=940-lift
  d.rounded_rectangle((px-57,py-90,px+57,py+100),radius=18,fill=CYAN)
  d.rounded_rectangle((px-43,py-70,px+43,py+70),radius=9,fill=BG)
  for dx in (-18,18):d.ellipse((px+dx-5,py-8,px+dx+5,py+2),fill=WHITE)
  d.arc((px-20,py+12,px+20,py+36),0,180,fill=YELLOW,width=5)
  if t>=3:
   for dx in (-98,98):d.line((px+dx*.65,py-50,px+dx,py-85),fill=YELLOW,width=8)
  txt(d,'A quick check. A little Chinese.',1510,47)
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
f=R/'2000_pocket_phone_rescue.mp4';print(json.dumps({'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
