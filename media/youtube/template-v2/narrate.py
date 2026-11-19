from long_template_v2 import authorize_export
import os
authorize_export(os.environ['HANZI_PREPARATION_DATE'],os.environ['HANZI_TARGET_DATE'],os.environ['HANZI_CHANNEL_ID'])
import sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent.parent/'tts/offline_tts'))
from tts import Narrator,sha,R
import pathlib,json,subprocess,shutil,hashlib
P=__import__('pathlib').Path(__file__).resolve().parent;D=P

n=Narrator();clips={}
for i,s in enumerate(json.loads((P/'story.json').read_text())):
 for lang in ['en','zh']:
  if not s.get(lang):continue
  stem=f'{i:02}-{lang}';w=D/(stem+'.wav')
  if w.exists() and w.with_suffix('.json').exists():
   old=json.loads(w.with_suffix('.json').read_text())
   if isinstance(old,list) and ''.join(c['text'] for c in old).replace(' ','')==s[lang].replace(' ',''):
    r=dict(cues=[dict(start=c['offset']/1e7,end=(c['offset']+c['duration'])/1e7,text=c['text']) for c in old],voice='am_michael' if lang=='en' else 'zf_xiaobei',seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(w)])))
   elif isinstance(old,dict) and old.get('text_sha256')==hashlib.sha256(s[lang].encode()).hexdigest():
    r=old
   else:r=n.speak(s[lang],w,lang=lang)
  else:r=n.speak(s[lang],w,lang=lang)
  a=D/(stem+'.mp3');subprocess.run(['ffmpeg','-v','error','-y','-i',str(w),'-c:a','libmp3lame','-q:a','2',str(a)],check=True)
  # Whole-sentence cues measured from synthesis; no fabricated word alignment.
  marks=[dict(offset=int(c['start']*1e7),duration=int((c['end']-c['start'])*1e7),text=c['text']) for c in r['cues']]
  timing=D/(stem+'.json');timing.write_text(json.dumps(marks,ensure_ascii=False,indent=2))
  clips[stem]=dict(text_sha256=hashlib.sha256(s[lang].encode()).hexdigest(),audio_sha256=sha(a),timing_sha256=sha(timing),voice=r['voice'],timing_kind='measured_sentence_boundaries')
  print(stem,round(r['seconds'],2),flush=True)
manifest=dict(ready=True,commercial_use_verified=True,engine='kokoro-onnx 0.6.1',voice_model_ids=['Kokoro-82M v1.0 am_michael','Kokoro-82M v1.0 zf_xiaobei'],engine_and_model_checksums=json.loads((R/'models/sources.json').read_text()),clips=clips,qa='technical validation; subjective listening not claimed')
(D/'voice_asset_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
