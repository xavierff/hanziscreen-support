from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True);ROOT=Path('/workspace/scratch/a80a755f3b22')
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def rider(d,x,y,panic=False):
 d.rounded_rectangle((x-35,y,x+35,y+35),radius=8,fill=YELLOW)
 d.ellipse((x-21,y-53,x+21,y-11),outline=WHITE,width=4)
 for dx in (-8,8):d.ellipse((x+dx-2,y-37,x+dx+2,y-33),fill=WHITE)
 d.line((x,y-10,x,y+10),fill=CYAN,width=5)
 if panic:
  d.line((x,y-7,x-30,y-40),fill=CYAN,width=5);d.line((x,y-7,x+30,y-40),fill=CYAN,width=5)
 else:d.line((x-20,y+5,x+20,y+5),fill=CYAN,width=5)
 for dx in (-22,22):d.ellipse((x+dx-7,y+29,x+dx+7,y+43),fill=WHITE)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(ROOT/'upload/IMG_5435.jpeg').convert('RGB');widget.thumbnail((540,960),Image.Resampling.LANCZOS)
out=R/'1646_tone_theme_park.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'fluffing_a_duck.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.7,afade=t=out:st=19.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<3:
  text(d,'MANDARIN HAS FOUR TONES.',45,31,CYAN);text(d,'ME: “ONLY FOUR?”',110,40,YELLOW)
  for j,s in enumerate(['ā','á','ǎ','à']):
   x=85+j*120;d.text((x-25,360),s,font=fonts[64],fill=[CYAN,YELLOW,PINK,WHITE][j])
  rider(d,270,600);text(d,'Sounds like a relaxing lesson.',810,28)
 elif t<11.5:
  index=min(3,int((t-3)/2.1));q=((t-3)%2.1)/2.1
  names=['HIGH + LEVEL','RISING','LOW, THEN RISING','FALLING'];marks=['ā','á','ǎ','à']
  text(d,'MY VOICE:',45,34,CYAN);text(d,names[index],110,38,YELLOW);text(d,marks[index],220,70)
  points=[]
  for i in range(101):
   z=i/100;x=65+410*z
   y=520 if index==0 else 680-260*z if index==1 else 470+230*math.sin(math.pi*z) if index==2 else 400+320*z
   points.append((x,y))
  d.line(points,fill=CYAN,width=9)
  x,y=points[min(100,int(q*100))];rider(d,x,y-38,index>0)
  text(d,'Tone practice = tiny theme park',850,28,PINK)
 elif t<15:
  text(d,'WHY DOES MY VOICE',45,36,CYAN);text(d,'NEED A SEATBELT?',110,42,PINK)
  rider(d,270,480,True);d.line((240,487,299,452),fill=WHITE,width=7)
  for j in range(5):
   a=t*3+j*1.25;d.ellipse((270+math.cos(a)*120,465+math.sin(a)*120,278+math.cos(a)*120,473+math.sin(a)*120),fill=YELLOW)
  text(d,'Language lesson.',760,34);text(d,'Unexpected amusement park.',820,29,YELLOW)
 elif t<17:
  im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 else:
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (45,135,270,390,480,555):review.append(im.resize((180,320)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,320))
for i,f in enumerate(review):sheet.paste(f,(i*180,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
