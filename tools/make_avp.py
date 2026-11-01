"""Compress the student AVP videos for the web and write content/avp.json.

Originals live outside the project (large 1080p files); the web copies are 540p H.264 with a poster image.
Run:  python tools/make_avp.py
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import imageio_ffmpeg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\client\Videos\New folder")
OUT = ROOT / "media" / "video"
IMG = ROOT / "media" / "img"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# file name -> (slug, title shown on the card)
VIDEOS = [
    ("SMART HELMET AVP.mp4", "smart-helmet-avp", "Smart Helmet"),
    ("Project MAIS AVP.mp4", "mais-avp", "Project MAIS"),
    ("PROJECT VVASAC FINAL.mp4", "vvasac-avp", "Project VVASAC"),
    ("HYSEIS.mp4", "hyseis-avp", "HYSEIS"),
    ("VISION.mp4", "vision-avp", "VISION"),
]

OUT.mkdir(parents=True, exist_ok=True)
items = []
for fname, slug, title in VIDEOS:
    src = SRC / fname
    if not src.exists():
        sys.exit(f"MISSING: {src}")
    dst = OUT / f"{slug}.mp4"
    if not dst.exists():
        print("encoding", fname, flush=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(src),
                        "-vf", "scale=-2:540", "-c:v", "libx264", "-crf", "32", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dst)], check=True)
    cap = cv2.VideoCapture(str(dst))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = round(frames / fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(min(8, seconds / 4) * fps))
    ok, frame = cap.read()
    cap.release()
    if not ok:
        sys.exit(f"could not read a frame from {dst}")
    h, w = frame.shape[:2]
    im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    im.thumbnail((800, 800))
    poster = f"{slug}-poster.webp"
    im.save(IMG / poster, "WEBP", quality=78, method=6)
    items.append({"slug": slug, "title": title, "file": f"{slug}.mp4", "poster": poster,
                  "w": w, "h": h, "pw": im.width, "ph": im.height, "seconds": seconds,
                  "mb": round(dst.stat().st_size / 1e6, 1)})
    print("done", slug, seconds, "s", items[-1]["mb"], "MB", flush=True)

data = {"title": "Science Investigatory Projects under my mentorship", "items": items}
(ROOT / "content" / "avp.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("avp.json written,", len(items), "videos,", round(sum(i["mb"] for i in items), 1), "MB")
