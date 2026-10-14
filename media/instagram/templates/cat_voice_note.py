from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
ROOT=Path('/workspace/scratch/a80a755f3b22')
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8'
fonts={s:ImageFont.truetype(str(ROOT/'run_0245/NotoSansCJKsc-Bold.otf'),s) for s in range(20,81)}
def text(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((540-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
def cat(d,x,y,r=65):
 d.polygon([(x-r,y-r*.4),(x-r*.85,y-r*1.4),(x-r*.2,y-r*.8)],fill=PINK)
 d.polygon([(x+r,y-r*.4),(x+r*.85,y-r*1.4),(x+r*.2,y-r*.8)],fill=PINK)
 d.ellipse((x-r,y-r,x+r,y+r),fill=PINK)
 for a in (-.4,.4):d.ellipse((x+a*r-5,y-15,x+a*r+5,y+3),fill=BG)
 d.polygon([(x-8,y+12),(x+8,y+12),(x,y+21)],fill=BG)
 for side in (-1,1):
  for j in (-1,0,1):d.line((x+side*25,y+20,x+side*(r+20),y+20+j*15),fill=WHITE,width=3)
def mic(d,x,y):
 d.rounded_rectangle((x-30,y-60,x+30,y+35),radius=28,fill=CYAN)
 d.arc((x-45,y-25,x+45,y+55),0,180,fill=WHITE,width=6)
 d.line((x,y+55,x,y+90),fill=WHITE,width=6);d.line((x-35,y+90,x+35,y+90),fill=WHITE,width=6)
poster=Image.open(ROOT/'run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
widget=Image.open(ROOT/'upload/IMG_5435.jpeg').convert('RGB');widget.thumbnail((345,748),Image.Resampling.LANCZOS)
out=R/'1443_cat_voice_note.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(ROOT/'run_1844/gallop_bounce.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.8,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(510):
 t=k/30;im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 if t<1.8:
  text(d,'CHINESE ON MY LOCK SCREEN.',20,29,CYAN);text(d,'CAT ON MY VOICE NOTE.',65,30,YELLOW)
  im.paste(widget,((540-widget.width)//2,140))
 elif t<5.5:
  text(d,'RECORDING A MANDARIN',45,32,CYAN);text(d,'THANK-YOU MESSAGE',100,34)
  text(d,'谢谢',210,78,YELLOW);text(d,'xièxie • THANK YOU',325,30)
  mic(d,270,555)
  for j in range(15):
   x=110+j*23;h=10+30*abs(math.sin(t*8+j));d.line((x,765-h,x,765+h),fill=CYAN,width=5)
  text(d,'Nice. Clear. Polite.',855,32,WHITE)
 elif t<9.5:
  text(d,'MY CAT:',45,34,PINK);text(d,'“OUR VOICE NOTE.”',105,38)
  mic(d,270,555)
  prog=min(1,(t-5.5)/1.2);cat(d,600-330*prog,395,90)
  # paw reaches the microphone as the cat interrupts
  d.rounded_rectangle((260,470,300,590),radius=20,fill=PINK)
  text(d,'喵！',675,78,PINK);text(d,'miāo • MEOW',795,32)
 else:
  text(d,'MESSAGE DELIVERED:',45,34,CYAN)
  d.rounded_rectangle((65,215,475,390),radius=30,outline=WHITE,width=4)
  text(d,'“谢谢…喵！”',245,54,YELLOW)
  cat(d,270,570,80)
  text(d,'Thank you.',740,38);text(d,'Featuring my cat.',805,38,PINK)
  text(d,'Unexpected guest vocalist.',875,26,CYAN)
 if t>=14:
  im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
  text(d,'START LEARNING CHINESE',25,30);text(d,'FREE',70,46,YELLOW)
  im.paste(poster,((540-poster.width)//2,150));d=ImageDraw.Draw(im)
  text(d,'Try Hanzi on Screen FREE',858,30,YELLOW);text(d,'Link in bio',910,26)
 if k in (25,100,235,350,465):review.append(im.resize((216,384)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
sheet=Image.new('RGB',(1080,384))
for i,f in enumerate(review):sheet.paste(f,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
