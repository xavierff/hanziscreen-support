from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent; ROOT=R.parent
BG='#091c38'; WHITE='#f5f7fc'; CYAN='#52d8ef'; YELLOW='#ffdf65'; PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(18,81)}
def txt(d,s,y,size=34,c=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]); assert b[2]-b[0]<515,(s,b)
 d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=c)
def person(d,x,y,bob=0):
 y+=bob;d.ellipse((x-35,y-85,x+35,y-15),fill=CYAN)
 for dx in (-12,12):d.ellipse((x+dx-3,y-61,x+dx+3,y-53),fill=BG)
 d.arc((x-13,y-52,x+13,y-32),0,180,fill=BG,width=3)
 d.line((x,y-15,x,y+100),fill=CYAN,width=12)
 d.line((x,y+100,x-45,y+155),fill=CYAN,width=12);d.line((x,y+100,x+45,y+155),fill=CYAN,width=12)
 d.line((x,y+20,x-70,y+65),fill=CYAN,width=10)
 # microphone
 d.line((x-70,y+65,x-90,y+20),fill=WHITE,width=10);d.ellipse((x-105,y-5,x-75,y+25),fill=PINK)
poster=Image.open(R/'poster.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(R/'widget.jpeg').convert('RGB');assert hashlib.sha256((R/'widget.jpeg').read_bytes()).hexdigest()=='11bde4877577ad9cc73be97c1bb8189b191024418cfc1856bafde0c842a5bfa2'
widget.thumbnail((540,960),Image.Resampling.LANCZOS)
out=R/'1200_karaoke_water_break.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1646/fluffing_a_duck_30s.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.7,afade=t=out:st=19.2:d=0.8','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','20',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(600):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<4:
  txt(d,'ME AT CHINESE KARAOKE',45,31,CYAN);txt(d,'“I rehearsed this.”',110,35,YELLOW)
  txt(d,'♪ INSTRUMENTAL INTRO ♪',270,25)
  person(d,280,570,8*math.sin(t*6))
  for i in range(5):
   h=25+35*(1+math.sin(t*6+i))/2;d.rectangle((110+i*70,800-h,140+i*70,800),fill=PINK)
 elif t<8:
  txt(d,'THE LYRICS START',45,38,PINK);txt(d,'YOUR TURN TO SING',160,27)
  d.rounded_rectangle((65,260,475,370),radius=20,outline=WHITE,width=3)
  txt(d,'朋友…',275,48,YELLOW);person(d,280,575)
  txt(d,'Suddenly… very thirsty.',825,31)
 else:
  txt(d,'MY ENTIRE PERFORMANCE:',45,29,CYAN)
  txt(d,'喝水',150,70,YELLOW);txt(d,'hē shuǐ • drink water',245,28)
  person(d,195,580)
  # Bottle grows comically large, keeping the singer busy for the entire verse.
  s=1+min(1,(t-8)/1.5)*1.3;w=45*s;h=110*s;x=355;y=650
  d.rounded_rectangle((x-w,y-h,x+w,y),radius=16,fill='#2873a8',outline=CYAN,width=5)
  d.rectangle((x-w*.5,y-h-25,x+w*.5,y-h),fill=WHITE)
  d.line((195,600,x-w,550),fill=CYAN,width=10)
  for i in range(3):d.arc((x-25,y-100+i*22,x+25,y-70+i*22),0,180,fill=CYAN,width=3)
  txt(d,'A hydration solo.',805,37,PINK)
  txt(d,'Not a single note. Fully hydrated.',870,24)
 if 15<=t<17:
  im=Image.new('RGB',(540,960),BG);im.paste(widget,((540-widget.width)//2,(960-widget.height)//2))
 elif t>=17:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  txt(d,'START LEARNING MANDARIN',25,28);txt(d,'FREE TO START',73,39,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',858,30,YELLOW);txt(d,'Link in bio',910,26)
 if k in (50,170,325,475,555):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
