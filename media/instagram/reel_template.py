from pathlib import Path
import json,subprocess,wave,numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).parent
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
C=str(P/'NotoSansCJKsc-Bold.otf')
BG='#101629';W='#fffdf6';R='#ff526d'
def font(n,cjk=False):return ImageFont.truetype(C if cjk else F,n)
def center(d,s,y,n=65,color=W,cjk=False):
 f=font(n,cjk);box=d.textbbox((0,0),s,font=f);d.text(((1080-box[2])/2,y),s,font=f,fill=color)
def face(d,mood):
 d.ellipse((360,710,720,1070),fill='#ffd574')
 if mood=='cool':
  d.rounded_rectangle((395,815,525,885),15,fill=BG);d.rounded_rectangle((555,815,685,885),15,fill=BG);d.line((520,840,560,840),fill=BG,width=15);d.arc((460,920,620,1000),0,180,fill=BG,width=12)
 else:
  for x in [460,620]:d.ellipse((x-18,830,x+18,868),fill=BG)
  d.ellipse((510,925,570,985),fill=BG)
def scene(name,lines,mood='cool',sub=None):
 im=Image.new('RGB',(1080,1920),BG);d=ImageDraw.Draw(im);d.rounded_rectangle((70,210,1010,1580),45,outline='#303b56',width=5)
 for s,y,n,col,cjk in lines:center(d,s,y,n,col,cjk)
 face(d,mood)
 if sub:center(d,sub,1400,39,R)
 im.save(P/(name+'.png'))
scene('s1',[('ME AFTER LEARNING',300,61,W,False),('你好',450,155,R,True),('nǐ hǎo = hello',640,44,W,False),('Basically fluent.',1180,70,W,False)],sub='Confidence has entered the chat.')
scene('s2',[('THEN SOMEONE',330,70,W,False),('REPLIES IN MANDARIN',450,63,R,False),('My brain',1180,65,W,False)],mood='shock',sub='Please wait...')
scene('s3',[('BRAIN.EXE',340,92,R,False),('HAS STOPPED WORKING',480,60,W,False),('Vocabulary loading',1180,58,W,False)],mood='shock',sub='One greeting. Unlimited confidence.')
scene('s4',[('PLOT TWIST',340,82,R,False),('I was fluent...',500,73,W,False),('in saying hello.',1180,76,W,False)],sub='We all start somewhere.')
# One unmodified genuine app-card crop from the approved screenshot poster.
src=Image.open('03_flashcards.jpg');crop=src.crop((680,593,1040,1130));crop.save(P/'app_crop.jpg')
im=Image.new('RGB',(1080,1920),BG);d=ImageDraw.Draw(im)
center(d,'Learn Chinese every time',250,57);center(d,'you unlock your phone',335,60)
d.rectangle((484,450,596,520),fill='#e72b3b');d.text((493,448),'★',font=font(37),fill='#ffd574')
crop=crop.resize((470,701));im.paste(crop,(305,610));center(d,'Download Hanzi on Screen',1410,56,R);center(d,'— Link in Bio',1500,62)
# Download-to-phone icon for the closing CTA.
d.rounded_rectangle((510,1640,570,1730),8,outline=W,width=5);d.line((540,1650,540,1700),fill=R,width=7);d.polygon([(523,1684),(557,1684),(540,1706)],fill=R)
im.save(P/'end.png')
parts=[('s1',4),('s2',4),('s3',4),('s4',5),('end',3)]
for name,sec in parts:
 vf="scale=1080:1920,setsar=1,format=yuv420p"
 if name=='s3':vf+=",drawbox=x=210:y=1310:w=660:h=18:color=0x303b56:t=fill,drawbox=x=210:y=1310:w=40:h=18:color=0xff526d:t=fill"
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(P/(name+'.png')),'-vf',vf,'-t',str(sec),'-r','30','-c:v','libx264','-preset','fast','-crf','21','-threads','2',str(P/(name+'.mp4'))],check=True)
(P/'concat.txt').write_text(''.join(f"file '{P/(name+'.mp4')}'\n" for name,sec in parts))
sr=44100;dur=20;t=np.arange(sr*dur)/sr;a=np.zeros_like(t)
for k in range(40):
 x=t-k*.5;m=(x>=0)&(x<.45);freq=[261.63,329.63,392,329.63][k%4];a[m]+=.085*np.sin(2*np.pi*freq*x[m])*np.exp(-10*x[m])
for st,f in [(4,280),(8,180),(12,523),(17,659)]:
 x=t-st;m=(x>=0)&(x<.3);a[m]+=.13*np.sin(2*np.pi*f*x[m])*np.exp(-14*x[m])
a*=np.clip((20-t)/.2,0,1)
with wave.open(str(P/'audio.wav'),'w') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-i',str(P/'audio.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(P/'hanzi_hello_confidence_1848.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'hanzi_hello_confidence_1848.mp4'),'-vf','fps=1/4,scale=216:384,tile=5x1','-frames:v','1',str(P/'check.jpg')],check=True)
print(json.dumps({'size':(P/'hanzi_hello_confidence_1848.mp4').stat().st_size,'duration':20}))
