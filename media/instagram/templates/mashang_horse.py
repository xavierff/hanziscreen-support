from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, hashlib, json, wave, struct

R=Path(__file__).parent; R.mkdir(parents=True,exist_ok=True)
W,H,FPS,DUR=540,960,30,17
BG='#091c38'; WHITE='#f5f7fc'; CYAN='#52d8ef'; YELLOW='#ffdf65'; CORAL='#ff7f78'; BROWN='#b67a45'
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
POSTER='/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,56,72)}

def center(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]); d.text(((W-(b[2]-b[0]))/2,y),s,font=fonts[size],fill=color)

def person(d,x,y,color,arm=0):
 d.ellipse((x-25,y-70,x+25,y-20),outline=color,width=5)
 d.ellipse((x-9,y-51,x-4,y-46),fill=WHITE); d.ellipse((x+6,y-51,x+11,y-46),fill=WHITE)
 d.arc((x-11,y-43,x+11,y-27),0,180,fill=color,width=3)
 d.line((x,y-20,x,y+70),fill=color,width=7)
 d.line((x,y+5,x-35,y+35),fill=color,width=7); d.line((x,y+5,x+42,y+15+arm),fill=color,width=7)
 d.line((x,y+70,x-25,y+118),fill=color,width=7); d.line((x,y+70,x+25,y+118),fill=color,width=7)

def horse(d,x,y,phase):
 # tail, body, neck, head
 d.arc((x-135,y-35,x-75,y+40),110,280,fill=BROWN,width=8)
 d.ellipse((x-105,y-60,x+95,y+55),fill=BROWN)
 d.polygon([(x+60,y-35),(x+115,y-115),(x+145,y-90),(x+95,y+20)],fill=BROWN)
 d.ellipse((x+102,y-132,x+172,y-74),fill=BROWN)
 d.polygon([(x+120,y-128),(x+127,y-160),(x+143,y-126)],fill=BROWN)
 d.ellipse((x+150,y-112,x+157,y-105),fill=BG)
 # legs gallop in opposing pairs
 swing=32*math.sin(phase)
 for lx,sgn in ((-65,1),(-20,-1),(35,-1),(75,1)):
  d.line((x+lx,y+35,x+lx+sgn*swing,y+110),fill=BROWN,width=10)
  d.line((x+lx+sgn*swing,y+110,x+lx+sgn*swing+20,y+126),fill=BROWN,width=9)
 # rider
 d.ellipse((x-18,y-142,x+28,y-96),outline=YELLOW,width=5)
 d.line((x+5,y-96,x+10,y-28),fill=YELLOW,width=7)
 d.line((x+10,y-70,x+68,y-80),fill=YELLOW,width=7)
 d.line((x+8,y-28,x-15,y+25),fill=YELLOW,width=7)

def audio(path):
 sr=44100; samples=[]
 melody=[392,494,587,494,440,523,659,523]
 for i in range(sr*DUR):
  t=i/sr; step=int(t*4); q=(t*4)%1
  n=melody[step%len(melody)]
  pluck=math.sin(2*math.pi*n*t)*math.exp(-8*q)
  # distinct clip-clop pair at 3 Hz
  hoof=(t*3)%1
  click=math.sin(2*math.pi*(900-500*hoof)*t)*math.exp(-38*hoof)
  off=(t*3+0.48)%1
  click2=math.sin(2*math.pi*(720-360*off)*t)*math.exp(-42*off)
  bass=math.sin(2*math.pi*(n/4)*t)*math.exp(-12*q)
  fade=1 if t<16.2 else max(0,(17-t)/0.8)
  v=(0.22*pluck+0.16*click+0.13*click2+0.12*bass)*fade
  samples.append(int(max(-1,min(1,v))*32767))
 with wave.open(str(path),'wb') as wf:
  wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes(struct.pack('<'+'h'*len(samples),*samples))

wav=R/'gallop_bounce.wav'; audio(wav)
poster=Image.open(POSTER).convert('RGB'); poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'1844_mashang_horse.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(wav),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.9','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
 if t<14:
  if t<3:
   center(d,'CHINESE TEACHER:',65,30,CYAN); center(d,'“COME HERE — 马上!”',118,40,YELLOW)
   person(d,110,570,CYAN,arm=-25)
   d.rounded_rectangle((220,345,485,610),radius=15,outline=WHITE,width=5)
   center(d,'马上',395,72,WHITE); center(d,'mǎshàng',490,34,CYAN);center(d,'right away',545,30)
  elif t<6:
   center(d,'马上  mǎshàng',75,46,YELLOW); center(d,'MEANS “RIGHT AWAY”',145,34)
   person(d,105,570,CYAN,arm=-25)
   # sound cue enters before horse
   for j in range(4):
    xx=305+j*45; yy=650+18*(j%2);d.arc((xx-18,yy-8,xx+18,yy+8),0,180,fill=CORAL,width=5)
   center(d,'clip... clop...?',820,30,CORAL)
  elif t<10.3:
   center(d,'BUT I HEARD:',55,30,CYAN)
   center(d,'马 = HORSE   上 = ON',105,40,YELLOW)
   prog=min(1,(t-6)/2.7); x=650-prog*550
   horse(d,x,600,t*10)
   # motion lines
   for j in range(5): d.line((x-180-j*25,610+j*18,x-115-j*25,610+j*18),fill='#45658a',width=4)
   center(d,'“ON A HORSE.”',820,40,WHITE)
  else:
   center(d,'TEACHER:',60,30,CYAN);center(d,'“I MEANT IMMEDIATELY.”',105,34)
   person(d,105,575,CYAN,arm=15)
   horse(d,350,620,t*8)
   d.rounded_rectangle((140,300,495,430),radius=25,fill=WHITE)
   center(d,'“I AM HERE 马上.”',325,34,BG)
   center(d,'Technically… very literal.',835,30,YELLOW)
 else:
  center(d,'START LEARNING CHINESE',25,30);center(d,'FREE',70,46,YELLOW)
  im.paste(poster,((W-poster.width)//2,150));d=ImageDraw.Draw(im)
  center(d,'Try Hanzi on Screen FREE',858,30,YELLOW);center(d,'Link in bio',910,26)
 if k in (45,125,230,345,465): review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0: raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'audio_size':wav.stat().st_size,'audio_sha256':hashlib.sha256(wav.read_bytes()).hexdigest()}))
