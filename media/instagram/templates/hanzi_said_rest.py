from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, hashlib, json, wave, struct, random

R = Path(__file__).parent
R.mkdir(parents=True, exist_ok=True)
W, H, FPS, DUR = 540, 960, 30, 17
BG, WHITE, CYAN, YELLOW, GREEN = '#091c38', '#f5f7fc', '#52d8ef', '#ffdf65', '#78df9b'
FONT = '/workspace/scratch/a80a755f3b22/run_0452/NotoSansCJKsc-Bold.otf'
POSTER = '/workspace/scratch/a80a755f3b22/run_1051/0B2C1F66-0943-4A60-9CD5-0616CC432ED0.jpeg'
fonts = {s: ImageFont.truetype(FONT, s) for s in (20, 24, 26, 30, 34, 40, 46, 56, 72, 96)}

def center(d, text, y, size=34, color=WHITE):
    b = d.textbbox((0, 0), text, font=fonts[size])
    d.text(((W - (b[2]-b[0]))/2, y), text, font=fonts[size], fill=color)

def stick(d, x, y, color, tired=False, lying=False):
    if lying:
        d.ellipse((x-100, y-35, x-45, y+20), outline=color, width=5)
        d.line((x-45, y-7, x+65, y-7), fill=color, width=7)
        d.line((x+65, y-7, x+105, y-28), fill=color, width=7)
        d.line((x+65, y-7, x+105, y+15), fill=color, width=7)
        return
    d.ellipse((x-28, y-75, x+28, y-19), outline=color, width=5)
    d.ellipse((x-11, y-53, x-5, y-47), fill=WHITE)
    d.ellipse((x+7, y-53, x+13, y-47), fill=WHITE)
    if tired:
        d.arc((x-12, y-41, x+12, y-25), 180, 360, fill=color, width=3)
    else:
        d.arc((x-12, y-43, x+12, y-25), 0, 180, fill=color, width=3)
    d.line((x, y-19, x, y+85), fill=color, width=7)
    d.line((x, y+15, x-40, y+40), fill=color, width=7)
    d.line((x, y+15, x+40, y+35), fill=color, width=7)
    d.line((x, y+85, x-30, y+135), fill=color, width=7)
    d.line((x, y+85, x+30, y+135), fill=color, width=7)

def tree(d, x, y, sway=0):
    d.rounded_rectangle((x-24, y-10, x+24, y+190), radius=10, fill='#9a6a42')
    d.ellipse((x-105+sway, y-115, x+105+sway, y+60), fill=GREEN)
    d.ellipse((x-80-sway, y-160, x+80-sway, y+15), fill='#62c987')

def make_audio(path):
    sr = 44100
    random.seed(7)
    samples = []
    notes = [261.63, 329.63, 392.00, 329.63, 293.66, 349.23, 440.00, 349.23]
    for i in range(int(sr*DUR)):
        t = i/sr
        beat = int(t*4)
        phase = (t*4) % 1
        note = notes[beat % len(notes)]
        pluck = math.sin(2*math.pi*note*t) * math.exp(-7*phase)
        bass = math.sin(2*math.pi*(note/2)*t) * math.exp(-10*phase)
        kick_phase = (t*2) % 1
        kick = math.sin(2*math.pi*(70-25*kick_phase)*t) * math.exp(-18*kick_phase)
        hat_phase = (t*4+0.5) % 1
        hat = (random.random()*2-1) * math.exp(-35*hat_phase)
        fade = 1 if t < 16.2 else max(0, (17-t)/0.8)
        v = max(-1, min(1, (0.24*pluck + 0.13*bass + 0.18*kick + 0.025*hat)*fade))
        samples.append(int(v*32767))
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(struct.pack('<' + 'h'*len(samples), *samples))

audio = R/'treehouse_breakbeat.wav'
make_audio(audio)
poster = Image.open(POSTER).convert('RGB')
poster.thumbnail((510, 700), Image.Resampling.LANCZOS)
out = R/'1649_hanzi_said_rest.mp4'
p = subprocess.Popen([
    'ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','pipe:0',
    '-i',str(audio),'-vf','scale=1080:1920:flags=lanczos','-af','volume=0.9',
    '-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',
    '-movflags','+faststart','-t',str(DUR),str(out)
], stdin=subprocess.PIPE)

review = []
for k in range(FPS*DUR):
    t = k/FPS
    im = Image.new('RGB', (W,H), BG)
    d = ImageDraw.Draw(im)
    if t < 14:
        if t < 2.6:
            center(d, 'MY CHINESE HOMEWORK:', 80, 34)
            center(d, 'MEMORIZE 休', 145, 56, YELLOW)
            # worksheet icon
            d.rounded_rectangle((165,285,375,550), radius=15, fill='#f5f7fc')
            d.line((200,350,340,350), fill='#b7c4d7', width=6)
            d.line((200,400,340,400), fill='#b7c4d7', width=6)
            d.text((225,435), '休', font=fonts[96], fill=BG)
        elif t < 6.2:
            center(d, 'HOW I REMEMBER IT:', 72, 34, CYAN)
            # components and scene
            d.text((78,215), '亻', font=fonts[96], fill=YELLOW)
            d.text((295,215), '木', font=fonts[96], fill=GREEN)
            center(d, 'person  +  tree', 330, 30)
            x = 120 + min(1,(t-2.6)/2.5)*105
            stick(d, x, 590, YELLOW, tired=True)
            tree(d, 385, 555, 2*math.sin(t*3))
            center(d, 'Just... one... more... word...', 850, 24, YELLOW)
        elif t < 9.8:
            center(d, 'PERSON + TREE', 66, 34, CYAN)
            tree(d, 350, 510, math.sin(t*3)*3)
            # leaning exhausted person
            stick(d, 235, 575, YELLOW, tired=True)
            d.line((235,590,315,555), fill=YELLOW, width=7)
            pop = min(1, (t-6.2)/0.6)
            size = int(56 + 40*pop)
            f = ImageFont.truetype(FONT, size)
            b = d.textbbox((0,0),'休',font=f)
            d.text(((W-(b[2]-b[0]))/2,190), '休', font=f, fill=WHITE)
            center(d, 'xiū  =  REST', 315, 40, GREEN)
        else:
            center(d, 'HOMEWORK:', 70, 30, CYAN)
            center(d, '“NEXT LESSON?”', 115, 40)
            # sleeping figure with blanket and tree
            tree(d, 420, 505, math.sin(t*2)*2)
            stick(d, 235, 650, YELLOW, lying=True)
            d.polygon([(115,665),(330,620),(380,780),(130,800)], fill='#315a8c')
            center(d, 'Sorry.', 320, 46, YELLOW)
            center(d, 'THE HANZI SAID REST.', 380, 40, WHITE)
            center(d, '休  xiū', 825, 34, GREEN)
    else:
        center(d, 'START LEARNING CHINESE', 25, 30)
        center(d, 'FREE', 70, 46, YELLOW)
        im.paste(poster, ((W-poster.width)//2, 150))
        d = ImageDraw.Draw(im)
        center(d, 'Try Hanzi on Screen FREE', 858, 30, YELLOW)
        center(d, 'Link in bio', 910, 26)
    if k in (45, 120, 225, 330, 465):
        review.append(im.resize((216,384)))
    p.stdin.write(im.tobytes())
p.stdin.close()
if p.wait() != 0:
    raise RuntimeError('render failed')
sheet = Image.new('RGB',(1080,384))
for i, frame in enumerate(review): sheet.paste(frame,(i*216,0))
sheet.save(R/'review.jpg')
print(json.dumps({
    'path': str(out), 'size': out.stat().st_size,
    'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'audio_size': audio.stat().st_size,
    'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest()
}))
