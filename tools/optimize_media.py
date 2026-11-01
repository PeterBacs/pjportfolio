"""Create web-optimised copies of the originals listed in content/media.json.

Originals are never modified. Output goes to media/ and media/manifest.json.
Requires: pillow, opencv-python-headless, reportlab  (pip install -r requirements-tools.txt)
"""
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media"
REG = json.loads((ROOT / "content" / "media.json").read_text(encoding="utf-8"))
manifest = {"images": {}, "videos": {}, "documents": {}, "og": {}}


def save_webp(img, path, quality=82):
    img.save(path, "WEBP", quality=quality, method=6)


def do_images():
    out = MEDIA / "img"
    out.mkdir(parents=True, exist_ok=True)
    for key, spec in REG["images"].items():
        src = ROOT / spec["src"]
        if not src.exists():
            sys.exit(f"MISSING ORIGINAL: {src}")
        im = Image.open(src)
        im = im.convert("RGBA" if spec.get("alpha") else "RGB")
        w0, h0 = im.size
        variants = []
        for w in sorted(set(min(w, w0) for w in spec["widths"])):
            h = round(h0 * w / w0)
            r = im.resize((w, h), Image.LANCZOS) if w != w0 else im
            name = f"{key}-{w}.webp"
            save_webp(r, out / name, 80 if spec["kind"] != "screenshot" else 88)
            variants.append({"w": w, "h": h, "file": name})
        manifest["images"][key] = {"variants": variants, "w": w0, "h": h0}
        print("img", key, [v["w"] for v in variants])


def do_og():
    """1200x630 social cards. Thumbnails are letterboxed (contain), never cropped."""
    out = MEDIA / "img"
    bg = (20, 23, 26)
    for key, spec in REG["images"].items():
        if not key.startswith("thumb-"):
            continue
        im = Image.open(ROOT / spec["src"]).convert("RGB")
        canvas = Image.new("RGB", (1200, 630), bg)
        scale = min(1200 / im.width, 630 / im.height)
        r = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        canvas.paste(r, ((1200 - r.width) // 2, (630 - r.height) // 2))
        name = f"og-{key[6:]}.jpg"
        canvas.save(out / name, "JPEG", quality=84, optimize=True)
        manifest["og"][key[6:]] = name
    # Home card: square portrait centred on its own backdrop colour, not cropped
    p = Image.open(ROOT / REG["images"]["peter"]["src"]).convert("RGB")
    corner = p.getpixel((8, 8))
    canvas = Image.new("RGB", (1200, 630), corner)
    sq = p.resize((630, 630), Image.LANCZOS)
    canvas.paste(sq, (285, 0))
    canvas.save(out / "og-home.jpg", "JPEG", quality=86, optimize=True)
    manifest["og"]["home"] = "og-home.jpg"


def do_videos():
    vdir = MEDIA / "video"
    vdir.mkdir(parents=True, exist_ok=True)
    for key, spec in REG["videos"].items():
        if not spec.get("publish"):
            print("video HELD BACK:", key, "-", spec.get("hold_reason"))
            continue
        src = ROOT / spec["src"]
        cap = cv2.VideoCapture(str(src))
        n, fps = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS)
        w, h = int(cap.get(3)), int(cap.get(4))
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * float(spec.get("poster_at", 0.25))))
        ok, frame = cap.read()
        cap.release()
        if not ok:
            sys.exit(f"cannot read frame from {src}")
        pw = min(1000, w)
        frame = cv2.resize(frame, (pw, round(h * pw / w)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(MEDIA / "img" / f"{key}-poster.webp"), frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
        shutil.copy2(src, vdir / f"{key}.mp4")
        manifest["videos"][key] = {
            "file": f"{key}.mp4", "poster": f"{key}-poster.webp", "w": w, "h": h,
            "seconds": round(n / fps), "bytes": (vdir / f"{key}.mp4").stat().st_size,
            "title": spec["title"],
        }
        print("video", key, manifest["videos"][key]["seconds"], "s")


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paras = [re.sub(r"<[^>]+>", "", p).strip() for p in xml.split("</w:p>")]
    return [p for p in paras if p]


def make_pdf(title, paras, out):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    from xml.sax.saxutils import escape

    h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=10)
    b = ParagraphStyle("b", fontName="Helvetica", fontSize=11, leading=16, spaceAfter=8)
    s = ParagraphStyle("s", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor="#555555")
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=25 * mm, rightMargin=25 * mm,
                            topMargin=25 * mm, bottomMargin=25 * mm, title=title, author="Peter John R. Bacani")
    story = [Paragraph(escape(title), h)] + [Paragraph(escape(p).replace("₂", "<sub>2</sub>"), b) for p in paras]
    story += [Spacer(1, 10), Paragraph("Text reproduced unchanged from the original Word document supplied by the author.", s)]
    doc.build(story)


def do_resume():
    """Render the résumé to page images for the view-only modal. The PDF itself is not published."""
    import pymupdf
    src = ROOT / REG["documents"]["resume"]["src"]
    doc = pymupdf.open(src)
    pages = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=170)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        name = f"resume-{i}.webp"
        img.save(MEDIA / "img" / name, "WEBP", quality=88, method=6)
        pages.append({"file": name, "w": pix.width, "h": pix.height})
    manifest["resume"] = {"pages": pages}
    stale = MEDIA / "docs" / REG["documents"]["resume"]["out"]
    if stale.exists():
        stale.unlink()
    print("resume pages", len(pages))


def do_ldm():
    """Render the Learning Delivery Modalities portfolio to page images for its view-only modal. The PDF itself is not published."""
    import pymupdf
    src = ROOT / REG["documents"]["ldm"]["src"]
    doc = pymupdf.open(src)
    pages = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        name = f"ldm-{i:02d}.webp"
        img.save(MEDIA / "img" / name, "WEBP", quality=80, method=6)
        pages.append({"file": name, "w": pix.width, "h": pix.height})
    manifest["ldm"] = {"pages": pages}
    print("ldm pages", len(pages))


def do_docs():
    ddir = MEDIA / "docs"
    ddir.mkdir(parents=True, exist_ok=True)
    for key, spec in REG["documents"].items():
        if not spec.get("publish"):
            continue
        src, dst = ROOT / spec["src"], ddir / spec["out"]
        if spec.get("convert"):
            make_pdf(spec["title"], docx_text(src), dst)
        else:
            shutil.copy2(src, dst)
        manifest["documents"][key] = {"file": spec["out"], "bytes": dst.stat().st_size}
        print("doc", key, dst.stat().st_size, "bytes")


if __name__ == "__main__":
    do_images()
    do_og()
    do_videos()
    do_docs()
    do_resume()
    do_ldm()
    (MEDIA / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print("manifest written")
