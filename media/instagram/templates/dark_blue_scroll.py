from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,hashlib
R=Path(__file__).parent
W,H,FPS,DUR=540,960,30,15
BG='#091c38';WHITE='#f5f7fc';CYAN='#52d8ef';YELLOW='#ffdf65'
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
fonts={s:ImageFont.truetype(FONT,s) for s in (22,26,30,34,40,46,70,100)}
poster=Image.open(R/'0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg').convert('RGB')
poster.thumbnail((510,700),Image.Resampling.LANCZOS)
def txt(d,s,y,size=34,color=WHITE):
 b=d.textbbox((0,0),s,font=fonts[size]);d.text(((W-b[2]+b[0])/2,y),s,font=fonts[size],fill=color)
out=R/'1051_checking_time.mp4'
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0','-i',str(R/'monkeys.mp3'),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.7,afade=t=out:st=14.3:d=0.7','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','15',str(out)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE);review=[]
for k in range(FPS*DUR):
 t=k/FPS; im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if t<12:
  if t<3:
   txt(d,'ME: JUST CHECKING',92,34);txt(d,'THE TIME.',145,46,CYAN)
  elif t<8:
   txt(d,'ONE REEL LATER...',90,40);txt(d,'REELS WATCHED',158,26,CYAN)
  else:
   txt(d,'REELS WATCHED: 47',90,34,CYAN);txt(d,'TIME CHECKED: 0',150,40,YELLOW)
  # Minimal phone character with rapidly scrolling abstract cards.
  d.rounded_rectangle((158,330,382,688),radius=28,fill='#163b63',outline=CYAN,width=5)
  d.rounded_rectangle((175,357,365,643),radius=12,fill='#102a4a')
  d.rounded_rectangle((225,338,315,348),radius=5,fill=BG)
  phase=max(0,t-3);speed=35+phase*80
  for j in range(4):
   y=365+((j*87-phase*speed)%270)
   if y<575:
    d.rounded_rectangle((187,y,353,y+62),radius=9,fill=('#20558a' if j%2 else '#226d87'))
    d.polygon([(253,y+16),(253,y+46),(280,y+31)],fill=CYAN)
  if 3<=t<8:
   count=min(47,1+int(46*((t-3)/5)**2))
   pulse=1+0.06*math.sin(t*2*math.pi/0.545)
   txt(d,str(count),228,100,YELLOW)
  # Thumb repeatedly swipes; eyes widen at the punchline.
  swipe=0 if t<3 or t>=8 else 35*math.sin(t*12)
  d.line((405,620,344,540+swipe),fill=YELLOW,width=26)
  d.ellipse((329,524+swipe,360,554+swipe),fill=YELLOW)
  d.line((178,690,148,751),fill=CYAN,width=8);d.line((362,690,392,751),fill=CYAN,width=8)
  if t>=8:
   d.ellipse((211,447,251,497),fill=WHITE);d.ellipse((286,447,326,497),fill=WHITE)
   d.ellipse((228,462,242,481),fill=BG);d.ellipse((303,462,317,481),fill=BG)
   d.arc((230,520,310,555),0,180,fill=YELLOW,width=7)
   txt(d,'Opened my phone.',772,30);txt(d,'Forgot why.',823,40,YELLOW)
   if t>=10:txt(d,'Let your Lock Screen teach Chinese.',893,22,CYAN)
  else:
   # Clock hands spin faster as scrolling takes over.
   d.ellipse((80,790,160,870),outline=CYAN,width=4)
   angle=(t if t<3 else t*6)
   d.line((120,830,120+28*math.sin(angle),830-28*math.cos(angle)),fill=WHITE,width=4)
   d.line((120,830,143,838),fill=YELLOW,width=4)
   txt(d,'POV: the accidental scrolling session',905,22)
 else:
  txt(d,'START LEARNING CHINESE',30,30);txt(d,'FREE',78,46,YELLOW)
  im.paste(poster,((W-poster.width)//2,158))
  d=ImageDraw.Draw(im);txt(d,'Try Hanzi on Screen FREE',865,30,YELLOW);txt(d,'Link in bio',916,26)
 if k in (30,180,270,405):review.append(im.resize((270,480)))
 p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0:raise RuntimeError('render failed')
v=Image.new('RGB',(1080,480))
for i,f in enumerate(review):v.paste(f,(i*270,0))
v.save(R/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
