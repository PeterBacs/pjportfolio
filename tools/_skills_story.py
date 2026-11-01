"""Rewrite sections A to H of the skills content as first-person statements that tie each skill to the projects that show it."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "content" / "skills.json"
T = ROOT / "content" / "techstack.json"
s = json.loads(P.read_text(encoding="utf-8"))

SUMMARY = {
    "embedded": "I build sensing, computing and display hardware that measures, processes and reports, and I have used it in the Smart Helmet and HYDRA.",
    "robotics": "I build microcontroller- and computer-controlled prototypes, I am trained in industrial automation (PLCs, SCADA and industrial robots), and I coach student robotics teams.",
    "ai": "I build models and image-analysis workflows that turn data into measurements, classifications and forecasts, and I have applied them in HYDRA, RETINA, VISION, HYSEIS and SAFARIS.",
    "design": "I check circuits and firmware in simulation before I build hardware, then I assemble and test the prototype at the bench.",
    "software": "I write the software that serves my models, stores and processes data, and presents results to engineers.",
    "research": "I turn a scientific question into defined, computable and testable quantities, and I have done this in RETINA and HYSEIS.",
}

D = {
    ("embedded", 0): "I program and interface Arduino and ESP32 microcontrollers and Raspberry Pi single-board computers as the sensing, control and processing core of my prototypes. In the Smart Helmet, a Raspberry Pi is the controller of a wearable that I coached my student team to build and on which I am a named inventor. In HYDRA, as project author, I joined sensors, cameras and a water dispenser in one kiosk.",
    ("embedded", 1): "I write C/C++ firmware and connect modules over I²C (Inter-Integrated Circuit), SPI (Serial Peripheral Interface) and UART (serial) links. In HYDRA, I connected the I²C-based MAX30102 pulse oximeter so that a finger pulse reading sits alongside the camera-based measurements.",
    ("embedded", 2): "I read physiological, gas, motion, environmental, distance and camera sensors and pass clean data to analysis software. The Smart Helmet uses an MQ-2 gas sensor, an accelerometer and a GPS module; HYDRA uses a MAX30102 sensor and cameras. I also work with temperature, humidity, light, ultrasonic and infrared distance sensors.",
    ("embedded", 3): "I build prototypes that collect data on the device, run the analysis locally or on a nearby computer, and report through a display, GPS location and a cellular GSM link. The Smart Helmet works this way: it monitors the wearer, analyses the readings and supports an emergency response. HYDRA analyses its measurements and reports the volume of water to dispense.",
    ("robotics", 0): "I connect sensors to actuators and coordinate them from one controller. In HYDRA, a single control system runs the cameras, the pulse sensor and the pump that dispenses the volume of water the analysis suggests.",
    ("robotics", 1): "I define the order in which a device senses, decides and acts. HYDRA follows a scan, analyse and dispense cycle, and the Smart Helmet keeps monitoring its wearer and raises an alert when it detects a problem.",
    ("robotics", 2): "I connect apps, data sources and devices into automated workflows, using triggers, API calls, data transformations, notifications and scheduled runs. I build them with tools such as n8n, Node-RED, Zapier and Make.",
    ("robotics", 3): "I have trained in programmable logic controllers (PLC), supervisory control and data acquisition (SCADA) systems and industrial robots. This extends the embedded control I do in my own prototypes to factory-style automation.",
    ("robotics", 4): "Before I build hardware, I simulate mobile robots, manipulators and perception pipelines in virtual environments. I use Gazebo with ROS 2 for mobile robots and navigation, NVIDIA Isaac Sim and Isaac Lab for AI robotics and learning-based control, CoppeliaSim for robot arms and custom robot prototypes, and Webots for teaching and research simulation.",
    ("robotics", 5): "I combine hardware, firmware and software into a working prototype, then test and debug it as a system. I did this myself as the author of HYDRA, and I guided my student team through the same prototyping and testing on the Smart Helmet.",
    ("robotics", 6): "I coach student teams in robotics and intelligent-machine competitions, and I have been recognised as a Winning Coach in Robotics and Intelligent Machine under the Department of Education.",
    ("ai", 0): "I train classifiers and forecasters on engineered features and historical data. In RETINA, I implemented a Random Forest (200 trees, depth 4, balanced class weights) on fractal features. HYDRA uses a Support Vector Machine on its combined measurements, and in HYSEIS I combined XGBoost with the Omori–Utsu and Gutenberg–Richter models to forecast aftershocks.",
    ("ai", 1): "I build and apply convolutional neural networks (CNNs) for image classification and U-Net models for segmentation, working in PyTorch and TensorFlow / Keras. VISION classifies medical images of the lungs, brain and skin with a CNN, and HYDRA uses U-Net segmentation on its eye scan.",
    ("ai", 2): "I develop image-processing workflows that isolate the relevant region and extract measurable features. In RETINA, I used OpenCV with CLAHE contrast enhancement, black-hat morphology and thresholding to isolate the vessel network and measure fractal and texture features. In my MATLAB skin-lesion tool, a photograph passes through grey conversion, enhancement, binarisation and segmentation before the tool reports Energy and Contrast values.",
    ("ai", 3): "I detect and localise objects in images. In HYDRA, I use YOLOv11 to find the urine reagent strip and its specific-gravity (SG) pad in the camera image.",
    ("ai", 4): "I label images with boxes, polygons and masks, then clean, split and version the datasets for training. For HYDRA, I annotated the urine test strips and their SG pads in CVAT, and I also work with Roboflow and Label Studio.",
    ("ai", 5): "I evaluate models with stratified k-fold cross-validation, confusion matrices, precision, recall and F1, and ROC / Youden's J cutoffs, as I did in RETINA. In VISION, I explain each prediction with a Grad-CAM heatmap, a probability chart and training curves.",
    ("ai", 6): "I have working knowledge of natural language processing, predictive modelling and anomaly detection, as I state in my skin-lesion project description.",
    ("design", 0): "I check circuit behaviour before I build it. I use LTspice for analog circuits, Logisim Evolution for digital logic design, and NI Multisim when I want analog and digital circuits in one environment.",
    ("design", 1): "I test firmware against a virtual circuit before I wire any hardware. I use Proteus VSM for firmware with its surrounding circuitry and Wokwi for Arduino, ESP32 and IoT projects online. I also use Tinkercad Circuits, SimulIDE, PICsimLab and Renode for real-time microcontroller, virtual-peripheral and emulated embedded-system work.",
    ("design", 2): "I model enclosures and mounts for my prototype hardware in CAD software such as SolidWorks and Fusion 360, and I check their fit before anything is made.",
    ("design", 3): "I assemble and test prototype hardware at the bench: the Smart Helmet's sensing and display unit, which my student team built under my coaching, and the HYDRA kiosk, which I authored. This rests on my BS in Electronics Engineering and Computer Science, my MS in Electronics and Telecommunications Engineering and my licence as a Registered Electronics Engineer.",
    ("software", 0): "I write Python for analysis and applications, C/C++ for microcontrollers, MATLAB for image processing, JavaScript for interfaces and SQL for data. RETINA is my clearest example: I wrote its Python, JavaScript and SQL myself, and my skin-lesion tool is built in MATLAB.",
    ("software", 1): "I build web applications that accept an upload, run a model or analysis and return the result. RETINA is a Flask application with 18 routes that I wrote, and I built the browser applications VISION and SAFARIS to work the same way.",
    ("software", 2): "I store analysis history and reference data in SQLite using SQL, process arrays with NumPy, export results to CSV, as in RETINA, and I also work with tables in pandas. I developed the School Information and Data Management System, which manages student records, attendance and grading.",
    ("software", 3): "I present results as dashboards, interactive maps, plots and printable reports. RETINA produces plots, PDF reports, a 12-step animated simulation and video export. HYSEIS shows its aftershock forecasts on an interactive Leaflet map, VISION shows probability charts, and the school system gives statistical dashboards of learners.",
    ("software", 4): "I turn models into quick demos and component-based interfaces with Streamlit, Gradio, React, TypeScript and Tailwind CSS.",
    ("software", 5): "I use version control, notebooks and scripting to keep my work organised and repeatable: Git and GitHub, Jupyter, VS Code, and PowerShell and Bash. In RETINA, I fix the random seeds so that the model results can be reproduced.",
    ("research", 0): "In RETINA, I implemented a box-counting fractal dimension (the least-squares slope of ln N(ε) against ln(1/ε)) and a 16-region local analysis of the vessel network. In HYSEIS, I applied the Omori–Utsu aftershock decay and Gutenberg–Richter magnitude–frequency models.",
    ("research", 1): "I frame measurable research questions and test the relationships between measures. In RETINA, I computed Pearson and Spearman correlations with p-values and r², standardised each deviation against a healthy reference with z-scores, and derived ROC / Youden's J cutoffs.",
    ("research", 2): "I design evaluations and compare my results against references: cross-validated metrics in RETINA, and worked example scenarios and runs in HYSEIS and my MATLAB tool. Each of my projects states whether its evidence is source code, a demonstration or a competition result.",
    ("research", 3): "I document designs, methods and results for different readers: project write-ups, a research study draft, a method article on how RETINA measures vessel complexity, and more than ten years of teaching engineering mathematics and mentoring student research.",
}

for sec in s["sections"]:
    if sec["id"] in SUMMARY:
        sec["summary"] = SUMMARY[sec["id"]]
    for i, c in enumerate(sec["capabilities"]):
        key = (sec["id"], i)
        if key in D:
            c["description"] = D[key]
            c.pop("context", None)
# enclosure card points to the engineering section
for sec in s["sections"]:
    if sec["id"] == "design":
        sec["capabilities"][2]["tools"] = ["SolidWorks", "Fusion 360"]
        sec["capabilities"][2]["links"] = [{"label": "Engineering design and fabrication", "url": "/skills/#engineering"}]
P.write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding="utf-8")

t = json.loads(T.read_text(encoding="utf-8"))
G = {
    "Languages and markup": "I write in these languages for firmware, analysis, interfaces and data work.",
    "Frameworks and servers": "I build web applications and automated workflows with these frameworks and servers. Flask runs my RETINA application.",
    "Databases": "I store and query data in these relational and document databases. RETINA keeps its analysis history in SQLite.",
    "Data science and machine learning": "I analyse data and train models with these numerical, plotting and deep-learning libraries and business-intelligence tools, as in RETINA, VISION and HYSEIS.",
    "Design and productivity": "I use these graphics, video, interface-design and documentation tools to present my work.",
}
for g in t["groups"]:
    if g["title"] in G:
        g["description"] = G[g["title"]]
T.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
print("rewritten", sum(1 for _ in D), "capabilities and", len(G), "tech groups")
