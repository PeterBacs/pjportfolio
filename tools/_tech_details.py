"""One-off: add a 'Technical details' section to every project page, and workflow-automation skills."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def save(p, d):
    (ROOT / p).write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


TECH = {
    "retina": [
        ["Language and web stack", "Python with a Flask web application (18 routes). JavaScript runs the upload interface and the 12-step animated simulation, which only plays back values computed in Python."],
        ["Image processing", "OpenCV: resize, green-channel extraction, CLAHE (clip limit 2.0, 8×8 tiles), Gaussian blur, black-hat morphology and thresholding. An optional manual threshold slider re-runs the real analysis."],
        ["Mathematical analysis", "NumPy: global box-counting dimension D from a least-squares fit of ln N(ε) against ln(1/ε), reported with R². A 4×4 grid gives 16 regions with local box sizes of 16, 8, 4 and 2 pixels, then the multifractal spread Δα, FD, MD and MAI."],
        ["Statistics", "SciPy: Pearson and Spearman correlations with p-values and r². z-score standardisation of deviations (MAIz). ROC / Youden's J cutoff from the user's labelled analyses."],
        ["Machine learning", "scikit-learn pipeline: StandardScaler and a Random Forest (200 trees, maximum depth 4, balanced class weights). Evaluated with stratified k-fold cross-validation (fixed random seed 42) for accuracy, precision, recall, F1 and a confusion matrix. Retrained from the current database on each use."],
        ["Data and outputs", "SQLite with analysis_results, healthy_reference and validated_threshold tables, plus CSV export. Matplotlib graphs and heatmaps, ReportLab PDF reports, and MP4 export of the simulation with OpenCV."],
    ],
    "hydra": [
        ["Image segmentation", "U-Net isolates the tear-meniscus region in each eye image. Six parameters are extracted: area, mean thickness, maximum thickness, curvature, continuity and intensity."],
        ["Object detection", "YOLOv11 detects the urine reagent strip and its specific-gravity (SG) pad. Training images were annotated in CVAT."],
        ["Classification", "A Support Vector Machine (SVM) combines the image-derived features with heart rate and SpO₂ to separate hydration categories."],
        ["Sensors and imaging", "MAX30102 optical sensor for heart rate and SpO₂. An enclosed eye-scan camera with uniform LED lighting, and a urine-strip camera with controlled lighting."],
        ["Hardware", "Touchscreen interface, filtered water reservoir, and a dispenser pump with its control system."],
    ],
    "smart-helmet": [
        ["Controller", "Raspberry Pi reads the sensors, runs the models and coordinates the outputs."],
        ["Sensors", "MQ-2 gas sensor for gas and alcohol, an accelerometer for head movement and impacts, and a GPS module for location."],
        ["Communication", "GSM module for cellular emergency alerts."],
        ["Display", "Backlit LCD in a pouch, connected to the helmet by cable."],
        ["Software intelligence", "Machine-learning models analyse the sensor data to identify potential safety risks, including fatigue, dizziness and alcohol."],
    ],
    "hyseis": [
        ["Forecasting models", "Omori–Utsu aftershock decay and the Gutenberg–Richter magnitude–frequency relation, combined with XGBoost to forecast aftershock probabilities and magnitudes from historical earthquake data."],
        ["Mapping", "Interactive Leaflet map on Esri World Imagery. OpenStreetMap Nominatim reverse geocoding gives epicentre addresses. A PHIVOLCS fault layer supports nearest-fault distance, fault length and endpoints."],
        ["Analysis views", "Magnitude and depth controls, time windows from 12 h to 30 d, and forecast or observed modes. Heatmap, pins, risk map and clickable grid cells, with an intensity legend from I to X."],
        ["Event report", "Ranked table of nearby towns with distance, intensity class, expected aftershocks and the probability of the event being felt at intensity IV or above."],
        ["Additional views", "Seismograph, shockwave and live-simulation views, and keyboard shortcuts for the main layers. The interface is served locally in the screenshots."],
    ],
    "safaris": [
        ["Application", "Browser-based web application with Crop, Fertilizer, Disease and Field pages, shown running on a local server."],
        ["Inputs", "Province selection for crop advice, soil nitrogen, phosphorus and potassium (NPK) values with the target crop for fertiliser advice, and a leaf-image upload for disease detection."],
        ["Outputs", "Recommended crop, fertiliser guidance, and a disease result that names the crop and disease with its cause and prevention steps (a corn example is shown)."],
        ["Machine learning", "Models for crop recommendation and plant-disease detection. The project folder holds model files, notebooks and a plant-disease image dataset, as seen in the demonstration video."],
    ],
    "vision": [
        ["Model", "Convolutional neural network (CNN) image classifier. The demonstration classifies a brain image as Normal or Brain Tumor and reports the probability."],
        ["Explainability", "Grad-CAM heatmap overlay highlights the image regions associated with the prediction, with a text explanation panel."],
        ["Training views", "Training-loss and training-accuracy plots appear alongside each prediction."],
        ["Interface", "Browser application served locally, with image upload, a probability bar chart, a live-detection option and an ID-scan field on the start screen."],
        ["Scope", "Designed for lung, brain and skin images."],
    ],
    "skin-lesion-matlab": [
        ["Platform", "MATLAB graphical interface with Train Database and Detect Melanoma functions."],
        ["Pipeline", "Input image, grey conversion, enhancement, binarisation, segmentation, then classification, with each stage shown side by side."],
        ["Measurements", "Energy and Contrast readouts, a boundary plot in the classification panel, and elapsed processing time."],
        ["Related work", "The project description also covers CNN architectures trained on large image databases for skin-cancer and tumour detection."],
    ],
    "school-information-system": [
        ["Application", "Web-based system for student records, attendance and grading."],
        ["Dashboards", "Statistical dashboard with donut and bar charts and tables of learners by grade level and gender."],
        ["Records", "Learner list with row-level actions, staff profile pages, and a faculty and staff gallery grouped by department."],
        ["Attendance and files", "ID-number scan screen with a live clock, and a file-manager login."],
    ],
}

for slug, rows in TECH.items():
    d = load(f"content/projects/{slug}.json")
    d["sections"] = [s for s in d["sections"] if s["id"] != "technical"]
    section = {"id": "technical", "title": "Technical details", "blocks": [
        {"type": "table", "caption": "Technology and methods", "headers": ["Area", "Technology and details"], "rows": rows}]}
    idx = 0
    for i, s in enumerate(d["sections"]):
        if s["id"] in ("overview", "contribution", "problem"):
            idx = i + 1
    d["sections"].insert(idx, section)
    save(f"content/projects/{slug}.json", d)

# ---- skills: workflow automation
sk = load("content/skills.json")
for sec in sk["sections"]:
    if sec["id"] == "robotics":
        sec["capabilities"] = [c for c in sec["capabilities"] if c["title"] != "Workflow and process automation"]
        new = {
            "title": "Workflow and process automation",
            "description": "Connect apps, data sources and devices into automated workflows with triggers, API calls, data transformations, notifications and scheduled runs.",
            "tools": ["n8n", "Node-RED", "Zapier", "Make", "Webhooks and APIs", "Scheduled jobs"],
            "projects": [],
            "review": "Which of these tools you use, and an example workflow (for example sensor data into a notification)."
        }
        pos = next(i for i, c in enumerate(sec["capabilities"]) if c["title"].startswith("Control logic")) + 1
        sec["capabilities"].insert(pos, new)
save("content/skills.json", sk)

roles = load("content/roles.json")
for r in roles["roles"]:
    if r["slug"] == "robotics-automation" and "n8n" not in r["tools"]:
        r["tools"].append("n8n")
save("content/roles.json", roles)
print("technical details and automation skills added")
