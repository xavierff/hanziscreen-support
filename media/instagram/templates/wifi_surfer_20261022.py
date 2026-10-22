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
# Original Wi-Fi Surf Stomp, no recordings or external samples.
rng=np.random.default_rng(2026102212)
for j,t in enumerate(np.arange(0,19.5,.32)):
 note(t,[220,329.63,440,392,293.66,440,523.25,329.63][j%8],.18,.09)
 if j%4 in (0,3):note(t,110,.12,.14)
for t in (0,.4,2.7,4,5.5,9,12,14,17):
 note(t,1318.51,.12,.10)
 i=int(t*sr);n=int(.2*sr);a[i:i+n]+=.02*rng.uniform(-1,1,n)*np.exp(-np.arange(n)/(sr*.05))
a*=np.minimum(1,(dur-np.arange(len(a))/sr)/.5)
with wave.open(str(R/'audio.wav'),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','pipe:0','-i',str(R/'audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(R/'1200_wifi_surfer.mp4')],stdin=subprocess.PIPE)
frames=[]
for k in range(fps*dur):
 t=k/fps;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<9:
  txt(d,'MANDARIN LEARNER PROBLEMS',185,37,CYAN)
  def surfer(x,y):
   d.ellipse((x-52,y-180,x+52,y-76),fill=YELLOW)
   d.line((x,y-75,x-30,y+70),fill=WHITE,width=20)
   d.line((x-8,y-30,x-115,y-12),fill=WHITE,width=18)
   d.line((x-5,y-30,x+100,y-75),fill=WHITE,width=18)
   d.line((x-30,y+65,x-120,y+130),fill=WHITE,width=18)
   d.line((x-30,y+65,x+90,y+125),fill=WHITE,width=18)
   d.ellipse((x-180,y+130,x+180,y+180),fill=PINK)
  if t<2.7:
   txt(d,'“Go online,” they said.',310,66)
   txt(d,'I brought a surfboard.',420,62,YELLOW)
  elif t<5.5:
   txt(d,'SURFING THE INTERNET.',310,61)
   txt(d,'The router wants a lifeguard.',420,49,YELLOW)
  else:
   txt(d,'上网 • shàngwǎng',310,76,YELLOW)
   txt(d,'go online / use the internet',430,49)
  for j in range(3):
   pts=[(x,1190+j*90+int(26*math.sin(x/150-t*5+j))) for x in range(90,1000,8)]
   d.line(pts,fill=CYAN,width=14)
  surfer(540+math.sin(t*3)*100,990+math.sin(t*5)*22)
  d.rounded_rectangle((275,1430,805,1570),radius=22,fill=WHITE)
  d.line((380,1430,340,1330),fill=WHITE,width=14)
  d.line((700,1430,740,1330),fill=WHITE,width=14)
  for j in range(4):d.ellipse((330+j*65,1490,348+j*65,1508),fill=CYAN)
  txt(d,'WI-FI: NOT WATERPROOF',1640,38)
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
f=R/'1200_wifi_surfer.mp4';print(json.dumps({'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
