from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent; W,H,FPS,DUR=540,960,30,16
BG='#091c38'; WHITE='#f5f7fc'; CYAN='#52d8ef'; YELLOW='#ffdf65'
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
fonts={s:ImageFont.truetype(FONT,s) for s in (20,24,26,30,34,40,46,64,100)}
poster=Image.open('/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB');poster.thumbnail((510,700),Image.Resampling.LANCZOS)
def txt(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
out=R/'1245_phone_teacher.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-ss','8','-i','/workspace/scratch/a80a755f3b22/run_1051/monkeys.mp3','-vf','scale=1080:1920:flags=lanczos','-af','volume=0.7,afade=t=out:st=15.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','16',str(out)],stdin=subprocess.PIPE)
review=[]
for k in range(FPS*DUR):
 t=k/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<13:
  if t<3:txt(d,'MY PHONE:',62,40);txt(d,'YOU AGAIN?',117,46,YELLOW)
  elif t<8:txt(d,'PHONE CHECKS',70,34,CYAN)
  elif t<10.5:txt(d,'FINE. I AM YOUR',65,34);txt(d,'CHINESE TEACHER NOW.',117,34,YELLOW)
  else:txt(d,'100 CHECKS.',65,46,CYAN);txt(d,'100 CHANCES TO SEE HANZI.',127,30,YELLOW)
  if t<8:
   count=min(100,1+int(99*(t/8)**2))
   txt(d,str(count),220,100,YELLOW)
  else:txt(d,'SAME HABIT. BETTER SIDE QUEST.',851,24)
  # Original anthropomorphic phone; screen is a cartoon face, not app UI.
  beat=math.sin(2*math.pi*t/0.545)
  bob=round(5*beat);x=160;y=370+bob
  d.rounded_rectangle((x,y,x+220,y+360),radius=30,fill='#163b63',outline=CYAN,width=5)
  d.rounded_rectangle((x+17,y+27,x+203,y+319),radius=12,fill='#102a4a')
  d.rounded_rectangle((x+67,y+8,x+153,y+17),radius=5,fill=BG)
  for ex in (225,309):
   if t<8:
    eyelid=16+int(13*(t/8));d.ellipse((ex-18,y+90,ex+18,y+130),fill=WHITE)
    d.ellipse((ex-5,y+105,ex+5,y+120),fill=BG)
    d.rectangle((ex-20,y+88,ex+20,y+90+eyelid),fill='#102a4a')
   else:
    d.ellipse((ex-16,y+88,ex+16,y+123),fill=WHITE);d.ellipse((ex-4,y+103,ex+4,y+119),fill=BG)
  d.arc((235,y+154,305,y+183),0 if t>=8 else 180,180 if t>=8 else 360,fill=YELLOW,width=6)
  d.line((180,y+360,149,y+410),fill=CYAN,width=7);d.line((360,y+360,391,y+410),fill=CYAN,width=7)
  if t<8:
   freq=2+t*1.4; tap=20*max(0,math.sin(t*freq*math.pi))
   d.line((433,y+245,372-tap,y+192),fill=YELLOW,width=24)
   d.ellipse((359-tap,y+177,385-tap,y+207),fill=YELLOW)
   if t>5:
    d.text((355,y+67),'?!',font=fonts[40],fill=YELLOW)
  else:
   # Teacher lifts a clearly cartoon chalkboard outside the phone.
   d.line((171,y+238,114,y+281),fill=CYAN,width=7)
   d.line((372,y+236,423,y+283),fill=CYAN,width=7)
   d.rounded_rectangle((103,y+216,437,y+341),radius=9,fill='#144f4e',outline=YELLOW,width=4)
   txt(d,'汉字  hànzì',y+219,40)
   txt(d,'Chinese characters',y+278,24)
  txt(d,'Illustrative phone-check count',914,20,'#a3b7d1')
 else:
  txt(d,'START LEARNING CHINESE',30,30);txt(d,'FREE',78,46,YELLOW)
  im.paste(poster,((W-poster.width)//2,158));d=ImageDraw.Draw(im)
  txt(d,'Try Hanzi on Screen FREE',865,30,YELLOW);txt(d,'Link in bio',916,26)
 if k in (30,210,345,435):review.append(im.resize((270,480)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
v=Image.new('RGB',(1080,480))
for i,f in enumerate(review):v.paste(f,(i*270,0))
v.save(R/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
