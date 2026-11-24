#!/usr/bin/env python3
"""Block semantically inconsistent Hanzi short-form source bundles before upload.

Run: python media/qa/check_short_source.py path/to/Hanzi_*_Source.zip [...]
All failures block Instagram, TikTok and YouTube Shorts distribution of that MP4.
Requires standard library only. Visual/linguistic editorial review remains required.
"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

STALE = re.compile(r"[\\\"'“‘](?:it[’']?s okay)[.!?]?[\\\"'”’]", re.I)

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower().replace("’", "'"))

def check(path):
    problems = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "RESUME.json" not in names:
            return ["missing canonical RESUME.json lesson manifest"]
        meta = json.loads(z.read("RESUME.json"))
        phrase = meta.get("phrase", "").strip()
        match = re.match(r"^(.+?。)\s*(.+?[.])\s*(.+)$", phrase)
        if not match:
            return ["phrase must provide Hanzi, tone-marked pinyin and English meaning"]
        hanzi, pinyin, english = (v.strip() for v in match.groups())
        scripts = [n for n in names if n.endswith(".py") and "/assets/" not in n]
        if len(scripts) != 1:
            return ["expected exactly one active rendering .py script"]
        script = z.read(scripts[0]).decode("utf-8", "replace")
        for kind, value in (("Hanzi", hanzi), ("pinyin", pinyin)):
            if value not in script:
                problems.append(kind + " lesson is not present in renderer: " + value)
        if norm(english) not in norm(script):
            problems.append("English meaning is not present in renderer: " + english)
        if norm(english) != "itsokay" and STALE.search(script):
            problems.append("stale 'It's okay' overlay for a DIFFERENT Mandarin meaning: " + english)
        # Older work mixed exactly the same cached English file across unrelated lessons.
        if "sample_2.wav" in script and "amix=inputs=3" in script:
            if "assets/sample_2.wav" not in names:
                problems.append("cached voice file missing")
            else:
                transcript = meta.get("english_voice_text", "").strip()
                expected_sha = meta.get("english_voice_sha256", "").strip()
                if not transcript or not expected_sha:
                    problems.append("mixed sample_2.wav requires verified English transcript and SHA256 for THIS lesson")
                else:
                    if hashlib.sha256(z.read("assets/sample_2.wav")).hexdigest() != expected_sha:
                        problems.append("English voice audio hash differs from approved manifest")
                    if norm(transcript) != norm(english):
                        problems.append("English voice text and canonical lesson meaning do not match")
        # Natural-looking English must not use full-width curly apostrophes
        # from a CJK-only font. A normal apostrophe is substantially narrower.
        if "NotoSansCJK" in script and re.search(r"[A-Za-z]+[’‘][A-Za-z]+", script):
            problems.append("English curly apostrophe is rendered with CJK font: use normal ASCII apostrophe and a Latin font")
        qa = meta.get("qa", {})
        if not qa.get("latin_typography_verified"):
            problems.append("English caption spacing/typography visual QA missing")
        if not qa.get("mandarin_voice_profile_approved"):
            problems.append("natural Mandarin voice preset/quality approval missing")
        if not qa.get("mandarin_voice_phrase_reviewed"):
            problems.append("Mandarin pronunciation/prosody QA for this phrase missing")
        if not meta.get("qa", {}).get("semantic_consistency_verified"):
            problems.append("semantic_consistency_verified editorial signoff missing")
    return problems

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    any_failure = False
    for name in sys.argv[1:]:
        try:
            errors = check(Path(name))
        except (OSError, ValueError, zipfile.BadZipFile) as e:
            errors = [str(e)]
        print(("BLOCK" if errors else "PASS") + ": " + name)
        for issue in errors:
            print(" - " + issue)
        any_failure |= bool(errors)
    return 1 if any_failure else 0

if __name__ == "__main__":
    sys.exit(main())
