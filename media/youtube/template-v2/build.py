from pathlib import Path
import json,subprocess,math,textwrap,hashlib,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from long_template_v2 import compose, authorize_export, make_thumbnail, VERSION
import os
R=Path(__file__).parent
authorize_export(os.environ['HANZI_PREPARATION_DATE'], os.environ['HANZI_TARGET_DATE'], os.environ['HANZI_CHANNEL_ID'])
EPISODE_ID=os.environ['HANZI_EPISODE_ID']
assert EPISODE_ID.replace('_','').isalnum(), 'Unsafe episode filename'
TITLE=os.environ['HANZI_TITLE']
assert 1 <= len(TITLE) <= 100 and '| Mandarin Story and Listening' not in TITLE
DATA=json.loads((R/'story.json').read_text());W,H=1280,720;FPS=15
FONT=R.parent/'bag/assets/NotoSansCJKsc-Regular.otf';fonts={s:ImageFont.truetype(str(FONT),s) for s in range(20,65)}
BG='#091c38';C='#52d8ef';Y='#ffdf65';P='#ff79a8';WHITE='#f5f7fc'
def probe(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
# OFFLINE ASSET GATE: this renderer never generates or transmits narration.
manifest_path=R/'voice_asset_manifest.json'
if not manifest_path.exists():
 raise RuntimeError('APPROVED_OFFLINE_NARRATION_NOT_READY: provide licensed, QA-approved local voice assets and manifest')
manifest=json.loads(manifest_path.read_text())
if manifest.get('ready') is not True or manifest.get('commercial_use_verified') is not True:
 raise RuntimeError('APPROVED_OFFLINE_NARRATION_NOT_READY: no approved licensed offline voice assets')
for i,scene in enumerate(DATA):
 for lang in ('en','zh'):
  if not scene.get(lang):continue
  stem=f'{i:02d}-{lang}';record=manifest.get('clips',{}).get(stem,{})
  audio=R/(stem+'.mp3');timing=R/(stem+'.json')
  expected_text=hashlib.sha256(scene[lang].encode('utf8')).hexdigest()
  if record.get('text_sha256')!=expected_text or not audio.is_file() or not timing.is_file():
   raise RuntimeError('MISSING_OR_MISMATCHED_APPROVED_NARRATION: '+stem)
  if hashlib.sha256(audio.read_bytes()).hexdigest()!=record.get('audio_sha256'):
   raise RuntimeError('AUDIO_HASH_MISMATCH: '+stem)
  if hashlib.sha256(timing.read_bytes()).hexdigest()!=record.get('timing_sha256'):
   raise RuntimeError('TIMING_HASH_MISMATCH: '+stem)
print('Verified licensed local narration assets',flush=True)
timeline=[];parts=[];cursor=0
for i,s in enumerate(DATA):
 start=cursor;cues=[]
 for lang in ('en','zh'):
  if not s.get(lang):continue
  mp=R/f'{i:02d}-{lang}.mp3';dur=probe(mp)
  boundaries=json.loads((R/f'{i:02d}-{lang}.json').read_text())
  for b in boundaries:cues.append({'start':cursor+b['offset']/1e7,'end':min(cursor+dur,cursor+(b['offset']+b['duration'])/1e7),'text':b['text'],'lang':lang})
  wav=R/f'{i:02d}-{lang}.wav'
  tmp=wav.with_suffix('.render.wav')
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(mp),'-ar','24000','-ac','1',str(tmp)],check=True)
  assert tmp.stat().st_size>44,('Incomplete decoded clip',tmp)
  tmp.replace(wav)
  parts.append(wav);cursor+=probe(wav)
  if lang=='en' and s.get('zh'):
   gap=R/'gap.wav'
   if not gap.exists():
    with wave.open(str(gap),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(b'\0\0'*7200)
   parts.append(gap);cursor+=.3
   if s.get('pre_pause'):
    q=R/f'{i:02d}-recall.wav'
    with wave.open(str(q),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(b'\0\0'*int(24000*s['pre_pause']))
    parts.append(q);cursor+=s['pre_pause']
 pause=s.get('pause',.45);sil=R/f'{i:02d}-pause.wav'
 with wave.open(str(sil),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(b'\0\0'*int(24000*pause))
 parts.append(sil);cursor+=pause
 timeline.append(dict(s,start=start,end=cursor,cues=cues,index=i))
with wave.open(str(R/'narration.wav'),'w') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000)
 for p in parts:
  with wave.open(str(p),'r') as r:f.writeframes(r.readframes(r.getnframes()))
dur=probe(R/'narration.wav');assert 180<=dur<=300,dur
(R/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2));print('Duration',dur,flush=True)

# Native landscape scenes expand the source Reel's character and palette.
# No permanent banner, footer, chapter card, border, or progress meter.
def center(d,text,y,size=34,color=WHITE):
 font=ImageFont.truetype(str(FONT),size)
 assert font.getlength(text)<W-140,(text,size)
 d.text((W/2,y),text,anchor='mt',font=font,fill=color,stroke_width=3,stroke_fill='#041023')
def wrap(text,size=31,width=1080):
 font=ImageFont.truetype(str(FONT),size);lines=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if font.getlength(test)>width and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 return lines
def actor(d,x,y,scale=1,happy=False,shirt=C):
 def box(a):return tuple((x+v*scale if i%2==0 else y+v*scale) for i,v in enumerate(a))
 d.rounded_rectangle(box((-48,55,48,170)),radius=int(20*scale),fill=shirt)
 for a in [(-30,162,-38,237),(30,162,40,237)]:d.line(box(a),fill=shirt,width=int(22*scale))
 d.ellipse(box((-45,-45,45,47)),fill='#ffd0ad')
 d.pieslice(box((-47,-52,47,27)),180,360,fill='#3a4667')
 for dx in [-15,15]:d.ellipse(box((dx-3,-4,dx+3,3)),fill=BG)
 d.arc(box((-15,11,15,31)),0 if happy else 180,180 if happy else 360,fill=BG,width=3)
 for a in [(-37,75,-82,122),(37,75,95,40)]:d.line(box(a),fill='#ffd0ad',width=int(16*scale))
def art(scene,phase,index):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,550,W,H),fill='#142c4b')
 for x in (398,585,772):
  d.rounded_rectangle((x,56,x+145,204),10,fill='#20364f',outline='#446480',width=4)
  for j in range(4):d.rounded_rectangle((x+11+j*31,83+j*4,x+32+j*31,183),4,fill=['#446c95','#555f83','#497880','#4d6885'][j])
 actor(d,207,270,1.02,index>1,C)
 if index:actor(d,1067,270,1.02,True,'#797bce')
 d.rounded_rectangle((355,510,923,542),12,fill='#56708a')
 for x in (400,880):d.line((x,540,x,642),fill='#56708a',width=12)
 if scene in ('example','question'):
  for x,col in [(498,'#5cb7e3'),(781,'#d57891')]:
   d.rounded_rectangle((x-79,243,x+70,290),16,fill=col)
   d.rounded_rectangle((x+35,265,x+76,345),12,fill=col)
 else:
  d.rounded_rectangle((453,242,826,351),12,fill='#6489b4',outline='#aec6e1',width=4)
  d.rounded_rectangle((469,234,810,332),12,fill='#ded8d6')
  d.line((640,241,640,328),fill='#738faa',width=4)
  for x,col,side in ((540,'#49b6eb',-1),(743,'#ffd55e',1)):
   if scene in ('return','twist'):x+=side*round(79*phase)
   if scene=='end' and side==1:x+=170
   y=210-round(31*math.sin(phase*math.pi)) if scene in ('return','twist') else 217
   d.polygon([(x-18,y),(x+18,y),(x+18,y+94),(x,y+81),(x-18,y+94)],fill=col)
   if side==1:d.text((x,y+25),'★',anchor='mm',font=fonts[20],fill=BG)
 if scene in ('listen','recall'):center(d,'?',61,58,Y)
 return im

GLOSS={'这是你的吗？': ('Zhè shì nǐ de ma?', 'Is this yours?'), '这是我的。': ('Zhè shì wǒ de.', 'This is mine.'), '这是你的。': ('Zhè shì nǐ de.', 'This is yours.'), '这是给你的。': ('Zhè shì gěi nǐ de.', 'This is for you.'), '谢谢你。': ('Xièxie nǐ.', 'Thank you.')}

def frame(s,t):
 return compose(s,t,art,GLOSS,FONT,R.parent/'bag/assets')[0]
checks=[]
for s in timeline:
 for c in s['cues']:
  im=frame(s,(c['start']+c['end'])/2)
  checks.append(dict(text=c['text'],start=c['start'],end=c['end'],fits=True))
(R/'caption_QA.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
# Inspect full-size frames and text bounds before the complete export.
for label,scene in [('opening',timeline[0]),('mid_dialogue',timeline[len(timeline)//2]),('two_line',timeline[1]),('teaching',timeline[2]),('ending',timeline[-1])]:
 cue=scene['cues'][-1] if label=='teaching' else scene['cues'][0]
 frame(scene,(cue['start']+cue['end'])/2).save(R/(label+'.jpg'))
make_thumbnail(art(timeline[0]['scene'],.2,0),FONT,os.environ['HANZI_THUMBNAIL_TEXT'],tuple(json.loads(os.environ['HANZI_THUMBNAIL_CROP']))).save(R/(EPISODE_ID+'_thumbnail.jpg'))
out=R/(EPISODE_ID+'.mp4')
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(R/'narration.wav'),'-c:v','libx264','-preset','fast','-crf','21','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(out)],stdin=subprocess.PIPE)
idx=0;shots=[]
for k in range(math.ceil(dur*FPS)):
 t=k/FPS
 while idx<len(timeline)-1 and t>=timeline[idx]['end']:idx+=1
 im=frame(timeline[idx],t);p.stdin.write(im.tobytes())
 if k%(FPS*20)==FPS:shots.append(im.resize((384,216)))
p.stdin.close();assert p.wait()==0
sheet=Image.new('RGB',(1152,216*math.ceil(len(shots)/3)),BG)
for i,im in enumerate(shots):sheet.paste(im,((i%3)*384,(i//3)*216))
sheet.save(R/'review.jpg')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
cues=[c for s in timeline for c in s['cues']]
(R/(EPISODE_ID+'.srt')).write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues)),encoding='utf8')
print(json.dumps({'path':str(out),'duration':dur,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}),flush=True)
