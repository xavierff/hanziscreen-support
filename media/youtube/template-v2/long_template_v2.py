"""Hanzi long-video export policy and caption compositor, version 2026-11-27.1."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import math

VERSION = "2026-11-27.1"
CHANNEL_ID = "UCnTFHhzyCoiSaDSfdGKFx5g"
ANCHOR = date(2026, 11, 22)

def wib_date(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("A datetime must include a timezone")
        return value.astimezone(ZoneInfo("Asia/Jakarta")).date()
    return value if isinstance(value, date) else date.fromisoformat(value)

def long_release_day(value):
    day = wib_date(value)
    return day >= ANCHOR and (day - ANCHOR).days % 3 == 0

def next_long_release(value):
    day = max(wib_date(value), ANCHOR)
    return day + timedelta(days=(-((day - ANCHOR).days)) % 3)

def authorize_export(preparation_day, target_day, channel_id):
    prep, target = wib_date(preparation_day), wib_date(target_day)
    if channel_id != CHANNEL_ID or not long_release_day(target) or target != prep + timedelta(days=1):
        raise ValueError("Long export requires the correct channel and the afternoon before an anchored release")

def latin_text(text):
    import unicodedata, re
    text=unicodedata.normalize('NFKC',text).replace('’',"'").replace('‘',"'").replace('“','').replace('”','')
    return re.sub(r'\s+', ' ', text).strip()

def caption_font_path(cjk_path, text):
    import re
    return cjk_path if re.search(r'[\u3400-\u9fff]',text) else Path(cjk_path).with_name('DejaVuSans.ttf')

def wrap_text(text, font, width):
    text=latin_text(text)
    lines, line = [], ""
    # English wraps at spaces. Chinese wraps at character boundaries.
    units = text.split() if " " in text else list(text)
    separator = " " if " " in text else ""
    for unit in units:
        trial = line + (separator if line else "") + unit
        if font.getlength(trial) > width and line:
            lines.append(line)
            line = unit
        else:
            line = trial
    if line:
        lines.append(line)
    if any(font.getlength(line) > width for line in lines):
        raise ValueError("A caption unit is wider than the safe area")
    return lines

def intersects(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

def caption_pages(text, start, end, font, width):
    lines = wrap_text(text, font, width)
    chunks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    weights = [sum(len(line) for line in chunk) for chunk in chunks]
    total, cursor, pages = sum(weights), start, []
    for i, (chunk, weight) in enumerate(zip(chunks, weights)):
        stop = end if i == len(chunks) - 1 else cursor + (end - start) * weight / total
        if stop - cursor < max(0.65, sum(len(s) for s in chunk) / 24):
            raise ValueError("Caption reading time is too short. Repair narration timing or copy.")
        pages.append(dict(start=cursor, end=stop, lines=chunk))
        cursor = stop
    return pages

def draw_captions(image, lines, font_path, protected=()):
    from PIL import Image, ImageDraw, ImageFont
    if not 1 <= len(lines) <= 2:
        raise ValueError("Speaking captions must use one or two lines")
    width, height = image.size
    lines=[latin_text(line) for line in lines]
    font = ImageFont.truetype(str(caption_font_path(font_path, ''.join(lines))), round(height * 0.050))
    gap = round(height * 0.012)
    boxes = [font.getbbox(line) for line in lines]
    line_height = max(b[3] - b[1] for b in boxes)
    block_height = len(lines) * line_height + (len(lines) - 1) * gap
    text_width = max(font.getlength(line) for line in lines)
    pad = round(height * 0.015)
    selected = None
    for bottom_fraction in (0.90, 0.76, 0.65):
        bottom = round(height * bottom_fraction)
        top = bottom - block_height
        box = (round((width - text_width) / 2) - pad, top - pad,
               round((width + text_width) / 2) + pad, bottom + pad)
        if all(not intersects(box, region) for region in protected):
            selected = (box, top)
            break
    if selected is None:
        raise ValueError("No safe caption position. Recompose the scene or its protected labels.")
    box, top = selected
    assert box[0] >= width * .05 and box[2] <= width * .95
    assert box[3] <= height * .92 and box[1] >= 0
    overlay = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(box, radius=round(height * .012), fill=(3, 13, 30, 215))
    for i, line in enumerate(lines):
        draw.text((width / 2, top + i * (line_height + gap)), line,
                  font=font, anchor="mt", fill="#f5f7fc", stroke_width=2, stroke_fill="#061329")
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    return image, dict(box=box, lines=lines, size=font.size, fallback=box[3] < height * .80)

def compose(scene, time, art, gloss, font_path, assets_dir):
    from PIL import Image, ImageDraw, ImageFont
    phase = (time - scene["start"]) / (scene["end"] - scene["start"])
    image = art(scene["scene"], phase, scene["index"])
    width, height = image.size
    # The legacy artwork used only the upper 550 rows of a 720 canvas.
    # Reframe the visual layer to use the canvas without adding footer padding.
    image = image.resize((width, round(height * 1.12))).crop((0, 0, width, height))
    if scene["scene"] == "end" and scene.get("show_app", False):
        for filename, x in (("owner_lock_screen_no_spice.jpeg", .02),
                            ("owner_ending_poster.jpeg", .85)):
            asset = Image.open(Path(assets_dir) / filename).convert("RGB")
            asset.thumbnail((round(width * .12), round(height * .31)))
            image.paste(asset, (round(width * x), round(height * .04)))
    cue = next((c for c in scene["cues"] if c["start"] <= time < c["end"]), None)
    last = next((c for c in reversed(scene["cues"]) if c["lang"] == "zh" and c["end"] <= time), None)
    teaching = cue if cue and cue["lang"] == "zh" else last if cue is None else None
    protected = [tuple(box) for box in scene.get("protected_regions", ())]
    evidence = None
    if teaching:
        chinese = teaching["text"]
        pinyin, meaning = gloss[chinese]
        # The featured teaching card is separate from the speaking-caption layer.
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(str(font_path), round(height * .064))
        draw.rounded_rectangle((width * .26, height * .49, width * .74, height * .61),
                               radius=12, fill="#132f50", outline="#52d8ef", width=2)
        draw.text((width / 2, height * .51), chinese, anchor="mt", font=font, fill="#ffdf65")
        protected.append((width * .25, height * .48, width * .75, height * .62))
        image, evidence = draw_captions(image, [pinyin, meaning], font_path, protected)
    elif cue:
        font = ImageFont.truetype(str(caption_font_path(font_path, cue["text"])), round(height * .050))
        pages = caption_pages(cue["text"], cue["start"], cue["end"], font, width * .84)
        page = next(page for page in pages if page["start"] <= time < page["end"])
        image, evidence = draw_captions(image, page["lines"], font_path, protected)
    return image, evidence

def make_thumbnail(scene_image, font_path, words, crop_box):
    """Use the episode's original close-up artwork and at most four words."""
    from PIL import ImageDraw, ImageFont
    if not 1 <= len(words.split()) <= 4:
        raise ValueError("Thumbnail text must contain one to four words")
    image = scene_image.crop(crop_box).resize((1280, 720))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(caption_font_path(font_path, words)), 95)
    if font.getlength(words) > 1120:
        raise ValueError("Thumbnail title exceeds the readable safe area")
    draw.text((640, 610), words, font=font, anchor="mm", fill="#ffdf65",
              stroke_width=7, stroke_fill="#041329")
    return image
