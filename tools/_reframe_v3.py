"""One-off: replace 'Limitations' sections with positive 'Next steps' framing and add search keywords."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "content" / "projects"


def load(slug):
    return json.loads((R / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, d):
    (R / f"{slug}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def set_section(d, sid, title, blocks, new_id=None):
    for s in d["sections"]:
        if s["id"] == sid:
            s["title"], s["blocks"] = title, blocks
            if new_id:
                s["id"] = new_id
            return
    d["sections"].append({"id": new_id or sid, "title": title, "blocks": blocks})


ul = lambda *items: {"type": "ul", "items": list(items)}
p = lambda t: {"type": "p", "text": t}

# ---- RETINA
d = load("retina")
set_section(d, "limitations", "Design notes and next steps", [
    ul("Intended use: research and education. The MAI describes structural deviation from a healthy reference and is not a clinical diagnosis.",
       "Reference calibration: every deviation score is computed against healthy images the user uploads, so the index sharpens as the reference set grows.",
       "Image input: clear, well-lit fundus photographs give the cleanest vessel maps."),
    p("Next steps: scale the evaluation to larger labelled datasets, report classification metrics, and benchmark the MAI against established vascular measures."),
], "next-steps")
d["keywords"] += " data science feature engineering analytical model statistics python numpy"
save("retina", d)

# ---- HYDRA
d = load("hydra")
set_section(d, "limitations", "Intended use and next steps", [
    ul("Intended use: hydration awareness for students and general wellness. It is not a diagnostic device."),
    p("Next steps: collect a larger labelled dataset across lighting conditions and skin tones, report classification metrics for each input, and compare the combined model with each single input."),
], "next-steps")
d["keywords"] += " computer vision multimodal sensor fusion yolo machine learning"
save("hydra", d)

# ---- HYSEIS
d = load("hyseis")
set_section(d, "limitations", "Next steps", [
    ul("Compare forecast probabilities with observed aftershock sequences and report calibration.",
       "Extend the fault database and the municipality-level intensity layers.",
       "Add more historical earthquake catalogues to the training data."),
], "next-steps")
d["keywords"] += " forecasting scientific modelling visualization time-series data science gis"
save("hyseis", d)

# ---- Smart Helmet
d = load("smart-helmet")
set_section(d, "limitations", "Next steps", [
    ul("Field testing across riding conditions and refinement of the fatigue, dizziness and alcohol-detection thresholds.",
       "Integration of emergency alerts with mobile and mapping services."),
], "next-steps")
for s in d["sections"]:
    if s["id"] == "implementation":
        for b in s["blocks"]:
            if b["type"] == "p":
                b["text"] = "The photographs show a white open-face helmet with a cable leading to a small pouch that holds a backlit LCD module."
save("smart-helmet", d)

# ---- SAFARIS
d = load("safaris")
set_section(d, "limitations", "Next steps", [
    ul("Field trials with farmers, and more crops, provinces and diseases in the recommendation models.",
       "Mobile-friendly and offline use for farms with weak connectivity."),
], "next-steps")
save("safaris", d)

# ---- VISION
d = load("vision")
set_section(d, "limitations", "Intended use and next steps", [
    ul("Intended use: decision support for screening. Final diagnosis stays with a qualified clinician."),
    p("Next steps: extend the lung and skin workflows to the same explainable interface, and report per-class precision, recall and ROC-AUC on held-out data."),
], "next-steps")
save("vision", d)

# ---- Skin
d = load("skin-lesion-matlab")
set_section(d, "limitations", "Related work and next steps", [
    p("This interface sits alongside broader work on CNN-based skin-cancer and tumour detection trained on large image databases, together with NLP, predictive modelling and anomaly detection."),
    p("Next steps: evaluate the pipeline on a public lesion dataset and compare its Energy and Contrast features with a CNN classifier."),
], "next-steps")
save("skin-lesion-matlab", d)

# ---- School system
d = load("school-information-system")
set_section(d, "limitations", "Next steps", [
    ul("Role-based access, audit logs and automated backups.",
       "Parent and student portals, and mobile attendance by QR code or ID card."),
], "next-steps")
save("school-information-system", d)
print("done")
