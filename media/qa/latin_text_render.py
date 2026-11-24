"""Normalize Latin text for Hanzi on Screen renderers.

Use on ENGLISH overlays before Pillow draw.text(). Keep Hanzi / Chinese
punctuation in their original Unicode form and render with a CJK font.
Do not use CJK-only fonts for English contractions.
"""
import re

_TRANSLATE = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": "", "\u201d": "",
    "\u00a0": " ", "\u2002": " ", "\u2003": " ", "\u2009": " ",
    "\u202f": " ", "\u200b": "",
})

def english_caption(text: str) -> str:
    """Normal display: 'It's okay.' not 'It’   s okay.'"""
    return re.sub(r" +", " ", text.translate(_TRANSLATE)).strip()

def has_hanzi(text: str) -> bool:
    return any("\u3400" <= char <= "\u9fff" for char in text)

def qa_english_caption(text: str) -> None:
    value = english_caption(text)
    if has_hanzi(value):
        raise ValueError("use separate Hanzi and English text layers/fonts")
    if any(ch in value for ch in "\u2018\u2019\u201c\u201d\u00a0\u200b"):
        raise ValueError("English overlay contains unusual punctuation/spacing")
    if len(value) == 0:
        raise ValueError("empty caption")

def render_english(draw, xy, text, font, *, fill, anchor="mt"):
    """font MUST be a proper Latin-family font, not NotoSansCJKsc."""
    qa_english_caption(text)
    draw.text(xy, english_caption(text), font=font, fill=fill, anchor=anchor)
