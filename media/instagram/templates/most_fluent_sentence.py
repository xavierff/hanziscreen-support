from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent;R.mkdir(parents=True,exist_ok=True)
W,H,FPS,DUR=540,960,30,17
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65';PINK='#ff79a8';GREEN='#78df9b'
FONT='/workspace/scratch/a80a755f3b22/run_0245/NotoSansCJKsc-Bold.otf'
POSTER='/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
AUDIO='/workspace/scratch/a80a755f3b22/run_1456/sneaky_snitch.mp3'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,56,72)}
def center(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-(b[2]-b[0]))/2,y),s,font=fonts[size],fill=color)
def person(d,x,y,color,mouth='smile',arm=0):
 d.ellipse((x-28,y-70,x+28,y-14),outline=color,width=5)
 d.ellipse((x-10,y-50,x-4,y-44),fill=WHITE);d.ellipse((x+7,y-50,x+13,y-44),fill=WHITE)
 if mouth=='o':d.ellipse((x-6,y-39,x+6,y-27),outline=color,width=3)
 elif mouth=='flat':d.line((x-10,y-31,x+10,y-31),fill=color,width=3)
 else:d.arc((x-12,y-42,x+12,y-24),0,180,fill=color,width=3)
 d.line((x,y-14,x,y+78),fill=color,width=7)
 d.line((x,y+10,x-40,y+35),fill=color,width=7);d.line((x,y+10,x+43,y+25+arm),fill=color,width=7)
 d.line((x,y+78,x-28,y+127),fill=color,width=7);d.line((x,y+78,x+28,y+127),fill=color,width=7)
poster=Image.open(POSTER).convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
out=R/'2249_most_fluent_sentence.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',AUDIO,'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.67,afade=t=out:st=16.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','17',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<14:
  if t<3.1:
   center(d,'THE ONE MANDARIN SENTENCE',60,30,CYAN);center(d,'I SAY PERFECTLY',110,46,YELLOW)
   person(d,270,540,YELLOW,mouth='smile',arm=-30)
   d.rounded_rectangle((95,285,445,410),radius=28,fill=WHITE)
   center(d,'READY. ASK ME ANYTHING.',320,24,BG)
   center(d,'Confidence: 100%',835,30,GREEN)
  elif t<7.1:
   center(d,'NATIVE SPEAKER:',55,30,CYAN)
   person(d,95,600,CYAN,mouth='o',arm=-20)
   d.rounded_rectangle((155,220,510,600),radius=30,fill=WHITE)
   d.text((185,260),'你周末想不想',font=fonts[40],fill=BG)
   d.text((185,330),'一起去吃火锅？',font=fonts[40],fill=BG)
   d.text((185,430),'nǐ zhōumò xiǎng bu xiǎng',font=fonts[20],fill='#315a8c')
   d.text((185,468),'yìqǐ qù chī huǒguō?',font=fonts[20],fill='#315a8c')
   for j in range(5):
    yy=690+j*35;xx=220+(j%2)*30;d.line((xx,yy,490-j*18,yy),fill='#45658a',width=4)
   center(d,'Sentence speed: native',860,26,PINK)
  elif t<10.2:
   center(d,'MY BRAIN:',60,34,CYAN)
   person(d,270,610,YELLOW,mouth='flat')
   d.rounded_rectangle((95,245,445,355),radius=22,outline=WHITE,width=5)
   d.rounded_rectangle((110,260,116,340),radius=3,fill=PINK)
   center(d,'LOADING… 2%',380,40,PINK)
   for j in range(8):
    a=t*5+j*math.pi/4;x=270+math.cos(a)*65;y=520+math.sin(a)*65
    d.ellipse((x-5,y-5,x+5,y+5),fill=WHITE if j<3 else '#45658a')
   center(d,'Vocabulary not responding.',845,26,YELLOW)
  else:
   center(d,'PERFECT ANSWER:',55,30,CYAN)
   person(d,110,625,YELLOW,mouth='smile',arm=-25)
   d.rounded_rectangle((155,240,505,520),radius=30,fill=WHITE)
   center(d,'我没听懂',285,56,BG);center(d,'wǒ méi tīng dǒng',375,26,CYAN);center(d,'I didn’t understand.',435,26,BG)
   # tiny trophy
   d.rectangle((245,650,295,700),fill=YELLOW);d.rectangle((225,700,315,720),fill=YELLOW)
   d.arc((205,640,255,695),90,270,fill=YELLOW,width=7);d.arc((285,640,335,695),270,90,fill=YELLOW,width=7)
   center(d,'Perfect pronunciation.',790,30,GREEN);center(d,'Zero information.',840,30,PINK)
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
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
