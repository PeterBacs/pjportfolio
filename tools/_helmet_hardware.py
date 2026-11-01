"""One-off: detailed Smart Helmet hardware and software."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def save(p, d):
    (ROOT / p).write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


# ---- project page
d = load("content/projects/smart-helmet.json")
d["tags"] = ["Raspberry Pi", "MQ-2 gas sensor", "GPS and GSM", "Machine learning"]
d["tech"] = ["Raspberry Pi", "MQ-2 gas sensor", "Accelerometer", "GPS module", "GSM module", "Machine learning", "Wearable sensors"]
d["keywords"] += " raspberry pi mq-2 gps gsm accelerometer wearable iot emergency alert"
for s in d["sections"]:
    if s["id"] == "architecture":
        s["title"] = "System overview"
        s["blocks"] = [{"type": "flow", "arrows": True, "caption": "", "steps": [
            {"label": "Sensors", "detail": "MQ-2 gas sensor, accelerometer and GPS module"},
            {"label": "Raspberry Pi", "detail": "Reads the sensors and runs the models"},
            {"label": "Machine-learning models", "detail": "Identify potential safety risks"},
            {"label": "Outputs", "detail": "LCD display and GSM emergency alert"}]}]
    if s["id"] == "implementation":
        s["title"] = "Hardware and software"
        s["blocks"] = [
            {"type": "p", "text": "The prototype is built around a Raspberry Pi that reads the helmet's sensors, runs machine-learning models on the data and drives the display and alerts."},
            {"type": "table", "caption": "Components", "headers": ["Component", "Role in the helmet"], "rows": [
                ["Raspberry Pi", "Main controller: reads the sensors, runs the machine-learning models and coordinates the outputs."],
                ["MQ-2 gas sensor", "Gas and alcohol sensing."],
                ["Accelerometer", "Measures head movement and sudden impacts."],
                ["GPS module", "Provides the helmet's location."],
                ["GSM module", "Cellular link for sending emergency alerts."],
                ["LCD display", "Backlit status display in a pouch, connected to the helmet by cable."],
                ["Machine-learning models", "Software intelligence that analyses the sensor data to identify potential safety risks, including fatigue, dizziness and alcohol."]]},
            {"type": "figure", "id": "helmet-2"},
        ]
save("content/projects/smart-helmet.json", d)

# ---- skills
s = load("content/skills.json")
for sec in s["sections"]:
    for c in sec["capabilities"]:
        t = c["title"]
        if t == "Microcontroller and single-board computer platforms":
            c["context"] = "Smart Helmet: Raspberry Pi controller, built by the mentored student team. HYDRA: project author."
            c["review"] = "Which board HYDRA uses, and whether Arduino and ESP32 appear in any project."
        if t == "Sensor integration":
            c["tools"] = ["MAX30102 pulse oximetry and heart rate", "MQ-2 gas and alcohol sensing", "Accelerometer", "GPS module", "Temperature, humidity and light", "Ultrasonic and infrared distance", "Camera modules"]
            c["context"] = "Shown in projects: MQ-2 gas sensor, accelerometer and GPS module (Smart Helmet); MAX30102 and cameras (HYDRA)."
            c["review"] = "Environmental and distance sensors have no project evidence."
        if t == "Connected devices and edge processing":
            c["description"] = "Build prototypes that collect data on the device, run analysis locally or on a nearby computer, and report through a display, GPS location and a cellular GSM link."
            c["tools"] = ["Raspberry Pi", "GPS module", "GSM module", "LCD and touchscreen displays", "TinyML / TensorFlow Lite"]
            c["review"] = "TinyML / TensorFlow Lite and any Wi-Fi, Bluetooth or MQTT use: confirm."
save("content/skills.json", s)

# ---- role page blurb
r = load("content/roles.json")
for role in r["roles"]:
    for p in role["projects"]:
        if p["slug"] == "smart-helmet" and role["slug"] == "electronics-embedded":
            p["why"] = "Raspberry Pi with MQ-2 gas, accelerometer, GPS and GSM modules, plus machine-learning risk analysis."
        if p["slug"] == "smart-helmet" and role["slug"] == "robotics-automation":
            p["why"] = "Continuous monitoring and GSM emergency-alert behaviour in a Raspberry Pi wearable."
    if role["slug"] == "electronics-embedded":
        role["tools"] = ["Raspberry Pi", "Arduino", "ESP32", "MQ-2", "GPS", "GSM", "I²C", "SPI", "UART", "Proteus VSM"]
save("content/roles.json", r)
print("updated")
