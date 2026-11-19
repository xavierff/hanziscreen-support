from pathlib import Path
import ast,json,math,subprocess,sys,wave,hashlib
from datetime import date,datetime
from PIL import Image,ImageDraw,ImageFont
from long_template_v2 import *
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'base/long'
FONT=ROOT.parent/'base/bag/assets/NotoSansCJKsc-Regular.otf'
W,H=1280,720
BG='#091c38';C='#52d8ef';Y='#ffdf65';P='#ff79a8';WHITE='#f5f7fc'
fonts={s:ImageFont.truetype(str(FONT),s) for s in range(20,65)}
# Load only the existing artwork functions. No legacy episode is re-exported.
tree=ast.parse((BASE/'build.py').read_text())
keep=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('center','wrap','actor','art')]
exec(compile(ast.Module(body=keep,type_ignores=[]),str(BASE/'build.py'),'exec'))
gloss=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GLOSS' for t in n.targets))
timeline=json.loads((BASE/'timeline.json').read_text())
for d in ('2026-11-22','2026-11-25','2026-11-28','2026-12-01'):assert long_release_day(d)
for d in ('2026-11-20','2026-11-21','2026-11-23'):assert not long_release_day(d)
assert next_long_release('2026-11-19')==date(2026,11,22)
authorize_export('2026-11-21','2026-11-22',CHANNEL_ID)
for prep,target,ch in [('2026-11-19','2026-11-20',CHANNEL_ID),('2026-11-21','2026-11-22','UCz1xZMze4b1zv-zwGE6dh8w')]:
 try:authorize_export(prep,target,ch)
 except ValueError:pass
 else:raise AssertionError('Unsafe export authorized')
records=[]
for s in timeline:
 for cue in s['cues']:
  times=[(cue['start']+cue['end'])/2]
  if cue['lang']=='en':
   pages=caption_pages(cue['text'],cue['start'],cue['end'],ImageFont.truetype(str(FONT),36),W*.84)
   assert pages[0]['start']==cue['start'] and pages[-1]['end']==cue['end']
   assert all(a['end']==b['start'] for a,b in zip(pages,pages[1:]))
   times=[(p['start']+p['end'])/2 for p in pages]
  for t in times:
   im,e=compose(s,t,art,gloss,FONT,ROOT.parent/'base/bag/assets')
   assert e and len(e['lines'])<=2
   records.append(dict(scene=s['scene'],time=t,**e))
# Explicit content-aware fallback when a real label occupies the bottom.
im=art('clue',.2,1)
im,e=draw_captions(im,['This caption moves above the protected label.'],FONT,[(350,530,930,690)])
assert e['fallback'];im.save(ROOT/'protected-object.jpg')
samples=[('opening',timeline[0],timeline[0]['cues'][0]),('mid-dialogue',timeline[3],timeline[3]['cues'][-1]),('two-line',timeline[0],timeline[0]['cues'][0]),('pinyin-card',timeline[6],timeline[6]['cues'][-1]),('ending',timeline[-1],timeline[-1]['cues'][-1])]
sheet=Image.new('RGB',(1280,1440),BG)
frames=[]
for i,(name,s,cue) in enumerate(samples):
 im,e=compose(s,(cue['start']+cue['end'])/2,art,gloss,FONT,ROOT.parent/'base/bag/assets')
 im.save(ROOT/(name+'.jpg'))
 for size in [(640,360),(320,180)]:im.resize(size).save(ROOT/(name+'-'+str(size[0])+'.jpg'))
 small=im.resize((640,360));sheet.paste(small,((i%2)*640,(i//2)*360))
 frames.append(im)
sheet.save(ROOT/'layout-evidence.jpg')
make_thumbnail(art('twist',.6,3),FONT,'WHOSE BOOKMARK?',(0,90,950,625)).save(ROOT/'thumbnail-template-test.jpg')
# One short test export uses approved existing English and Mandarin audio.
audio=BASE/'02-en.mp3'
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(audio)]))
out=ROOT/'layout-test.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','10','-i','pipe:0','-i',str(audio),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)],stdin=subprocess.PIPE)
scene=timeline[2];cue=scene['cues'][0]
for i in range(math.ceil(duration*10)):
 t=min(cue['end']-.001,cue['start']+i/10)
 im,_=compose(scene,t,art,gloss,FONT,ROOT.parent/'base/bag/assets')
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
result=dict(version=VERSION,cadence='pass',caption_pages=len(records),overlap='pass',full_test_decode='pass',cached_audio_sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),fresh_narration=False,full_episode_export=False,representative_sizes=[1280,640,320],source='build.py imports long_template_v2.compose and authorize_export')
(ROOT/'test-results.json').write_text(json.dumps(result,indent=2))
(ROOT/'caption-bounds.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(result)
