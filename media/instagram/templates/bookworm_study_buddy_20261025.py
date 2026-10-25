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
# Original Paper Snack Swing, synthesized without third-party samples.
for j,t in enumerate(np.arange(0,19.5,.37)):
 note(t,[349.23,440,523.25,659.25,587.33,523.25,440,261.63][j%8],.19,.08)
 if j%3==0:note(t,87.31,.18,.14)
for t in (0,.5,1,1.5,3,3.5,4,5.5,9,12,14,17):note(t,740,.12,.11)
a*=np.minimum(1,(dur-np.arange(len(a))/sr)/.5)
with wave.open(str(R/'audio.wav'),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-i',str(R/'audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(R/'1200_bookworm_study_buddy.mp4')],stdin=subprocess.PIPE)
frames=[]
for k in range(fps*dur):
 t=k/fps;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<9:
  txt(d,'MANDARIN MINI MOMENTS',180,43,CYAN)
  if t<3:
   txt(d,'I asked a bookworm to help.',300,56)
   txt(d,'It ate chapter one.',410,66,YELLOW)
  elif t<6:
   txt(d,'Great appetite.',300,69)
   txt(d,'Terrible tutor.',410,69,YELLOW)
  else:
   txt(d,'书虫 shūchóng = bookworm',300,56,CYAN)
   txt(d,'A person who loves reading.',420,50,YELLOW)
  # Literal cartoon worm eats a book: figurative phrase, not real behaviour.
  d.rounded_rectangle((210,850,870,1320),radius=28,fill=PINK)
  d.rectangle((235,870,845,1280),fill=WHITE)
  d.line((540,880,540,1270),fill='#a6bfd2',width=8)
  for j in range(5):
   yy=930+j*59
   d.line((285,yy,485,yy),fill='#7693ac',width=7)
   d.line((595,yy,800,yy),fill='#7693ac',width=7)
  bite=min(int(t*1.8),8)
  for j in range(bite):
   d.ellipse((720+(j%3)*36,890+(j//3)*68,820+(j%3)*36,990+(j//3)*68),fill=BG)
  hx=540+math.sin(t*3)*36;hy=740+math.sin(t*5)*15
  for j in range(5):
   xx=hx-j*57;yy=hy+math.sin(t*5-j)*20
   d.ellipse((xx-47,yy-45,xx+47,yy+45),fill='#75dfb0')
  d.ellipse((hx-62,hy-65,hx+62,hy+65),fill='#75dfb0')
  for dx in (-22,22):d.ellipse((hx+dx-7,hy-20,hx+dx+7,hy-5),fill=BG)
  d.arc((hx-24,hy+6,hx+24,hy+36),0,180,fill=BG,width=6)
  if int(t*3)%2==0:d.rectangle((hx-18,hy+36,hx+18,hy+73),fill=WHITE)
  txt(d,'Literal cartoon. Figurative phrase.',1510,43)
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
f=R/'1200_bookworm_study_buddy.mp4';print(json.dumps({'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
