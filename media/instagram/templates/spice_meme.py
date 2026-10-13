import math, subprocess, sys, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).parent
W,H,FPS,DURATION=540,960,30,16
FONT='/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
SHOT='/workspace/scratch/a80a755f3b22/run_0452/5d4f69c5-197f-4ba7-82af-847df2770592.jpeg'
sheet=Image.open(sys.argv[1]).convert('RGB')
panels=[sheet.crop((round(i*sheet.width/3),0,round((i+1)*sheet.width/3),sheet.height)) for i in range(3)]
shot=Image.open(SHOT).convert('RGB'); shot.thumbnail((350,755))
fonts={s:ImageFont.truetype(FONT,s) for s in (24,28,30,32,36,40,44)}

def text(d,txt,y,size=30,color='#143e38',box=False):
    font=fonts[size]; bbox=d.textbbox((0,0),txt,font=font)
    x=(W-(bbox[2]-bbox[0]))/2
    if box: d.rounded_rectangle((x-12,y-5,x+bbox[2]-bbox[0]+12,y+size+14),radius=10,fill='#143e38')
    d.text((x,y),txt,font=font,fill=color)

out=ROOT/'0844_spice_confidence.mp4'
audio="aevalsrc=0.04*sin(2*PI*180*t)*lt(mod(t\\,0.5)\\,0.07)+0.02*sin(2*PI*760*t)*lt(mod(t\\,1)\\,0.04):s=48000:d=16"
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(FPS),'-i','pipe:0','-f','lavfi','-i',audio,'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart','-t','16',str(out)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
frames=[]
for k in range(FPS*DURATION):
    t=k/FPS
    im=Image.new('RGB',(W,H),'#fff4e2'); d=ImageDraw.Draw(im)
    if t<13:
        idx=0 if t<6 else 1 if t<8 else 2
        local=t-(0 if idx==0 else 6 if idx==1 else 8)
        zoom=1.0+0.025*math.sin(local*3)
        if idx==1: zoom=1.0+0.12*min(local,1)
        sz=round(540*zoom); art=panels[idx].resize((sz,sz),Image.Resampling.LANCZOS)
        shake=round(10*math.sin(local*30)) if idx==2 else round(3*math.sin(local*3))
        bob=round(7*math.sin(local*4))
        im.paste(art,((W-sz)//2+shake,270+bob))
        d=ImageDraw.Draw(im)
        if t<3:
            text(d,'ME: I CAN ORDER',65,36)
            text(d,'IN MANDARIN.',120,40)
            text(d,'Confidence level: 100%',855,28)
        elif t<6:
            text(d,'微辣，谢谢。',65,44)
            text(d,'wēi là, xièxie',132,28)
            text(d,'A little spicy, thank you.',190,28)
        elif t<8:
            text(d,'ONE BITE LATER...',90,36)
        else:
            text(d,'MY MANDARIN: CONFIDENT',60,28)
            text(d,'MY SPICE TOLERANCE:',115,28)
            text(d,'OFFLINE',164,44,'#d93626')
            text(d,'Should have learned 不辣 first.',851,28)
            text(d,'bù là = not spicy',901,24)
            for j in range(7):
                x=90+j*60+12*math.sin(t*6+j)
                y=760-((t*120+j*45)%360)
                d.ellipse((x,y,x+12,y+22),fill='#55bbe0')
    else:
        text(d,'START LEARNING MANDARIN',37,28)
        text(d,'FREE',82,44,'#d93626')
        im.paste(shot,((W-shot.width)//2,155))
        d=ImageDraw.Draw(im)
        text(d,'Try Hanzi on Screen FREE',850,28,'white',True)
        text(d,'Link in bio',910,28)
    if k in (30,120,285,435): frames.append(im.copy().resize((270,480)))
    p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait()!=0: raise RuntimeError('Encoding failed')
review=Image.new('RGB',(1080,480))
for i,f in enumerate(frames): review.paste(f,(i*270,0))
review.save(ROOT/'review.jpg')
print(json.dumps({'path':str(out),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
