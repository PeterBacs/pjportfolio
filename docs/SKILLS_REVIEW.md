# Skills page review

Generated from `content/skills.json` by `tools/make_skills_review.py`.

## Evidence used
- **Source code**: RETINA (Python, NumPy, OpenCV, SciPy, scikit-learn, Matplotlib, SQLite, Flask, ReportLab).
- **Demo video**: RETINA, VISION, SAFARIS, the school system and the Smart Helmet news feature.
- **Screenshots / prototype images**: HYSEIS, the MATLAB tool, HYDRA, Smart Helmet.
- **Competition award**: Smart Helmet (SIIF 2024, SIBOL).
- **Your messages**: Arduino, ESP32, Raspberry Pi, the simulator list, YOLOv11 and CVAT on HYDRA. These are shown without a project link unless a project document supports them.

No capability is labelled 'validated', because no reported evaluation metrics were supplied.

## Claims that need your confirmation

### A. Embedded Systems and IoT
- **Microcontroller and single-board computer platforms**: Which board HYDRA uses, and whether Arduino and ESP32 appear in any project.
- **Firmware and hardware interfaces**: C/C++ and the three buses come from your request; confirm where each was used.
- **Sensor integration**: Environmental and distance sensors have no project evidence.
- **Connected devices and edge processing**: TinyML / TensorFlow Lite and any Wi-Fi, Bluetooth or MQTT use: confirm.

### B. Robotics, Automation and System Integration
- **Sensor and actuator integration**: Motors and servos have no project evidence.
- **Control logic and automated operating sequences**: Smart Helmet alert thresholds: confirm how they are set.
- **Workflow and process automation**: Which of these tools you use, and an example workflow (for example sensor data into a notification).
- **Industrial automation (training)**: Where and when you trained, which PLC brand and language (for example ladder logic), which SCADA software and robot brand, and any certificate. Industrial experience is not claimed.
- **Robotics software and simulation**: No project uses these. Confirm which you have run and to what depth, especially Isaac Lab.

### C. Artificial Intelligence, Machine Learning and Computer Vision
- **Deep learning**: Which project used PyTorch and which used TensorFlow/Keras; training details.
- **Object detection**: Detection details come from your message: confirm the training data and results.
- **Data annotation and dataset preparation**: Roboflow and Label Studio use; dataset sizes.
- **Wider machine-learning topics**: Confirm the depth; this is a statement of understanding rather than a project.

### D. Electronics Design, Prototyping and Simulation
- **Analog and digital circuit simulation**: No project evidence for the simulators; add an example circuit if you have one.
- **Microcontroller and firmware simulation**: You confirmed Wokwi and Proteus VSM; Tinkercad, SimulIDE, PICsimLab and Renode were my suggestions. Keep only those you use.
- **Enclosure and mechanical design**: Which CAD software, and an example part or enclosure.

### E. Programming, Applications and Data Systems
- **Model-serving applications**: Framework used in VISION and SAFARIS.
- **Databases and data handling**: pandas is not used in the RETINA source; confirm where you have used it.
- **Rapid demos and front-end frameworks**: Condensed from the earlier 16-card list. No project evidence; keep only the tools you have used.
- **Development workflow**: Git/GitHub, Jupyter and VS Code use: no repository history was supplied.

## Roles stated on the page (please confirm)
- Smart Helmet: mentor of the student team.
- HYDRA, HYSEIS, SAFARIS: project author (tasks not itemised).
- RETINA: implemented by you, based on the source code in your working folder.

## Coverage of every earlier skill

| Earlier skill | Status | Where it went, or why |
|---|---|---|
| PyTorch and TensorFlow / Keras | Retained, flagged | C. Deep learning. Not mapped to a project because no source or document shows which one was used. |
| Convolutional neural networks | Retained | C. Deep learning (VISION). |
| U-Net segmentation | Retained | C. Deep learning (HYDRA). |
| Support Vector Machines / Gradient boosting (XGBoost) / Random Forest and scikit-learn | Consolidated | C. Classical machine learning, with the project-specific method named. |
| Model evaluation | Retained, narrowed | C. Model evaluation: only methods found in the RETINA source (stratified k-fold, confusion matrix, precision/recall/F1, ROC / Youden's J). |
| Hyperparameter tuning | Removed | No tuning code or document found. Re-add if you tuned models and can name the method. |
| Time-series and predictive modelling | Consolidated | C. Classical machine learning (HYSEIS forecasting) and C. Wider topics. |
| Anomaly detection and NLP | Retained, relabelled | C. Wider topics, labelled 'stated understanding' from the skin-lesion description. |
| Reinforcement and imitation learning | Removed | No evidence. Isaac Lab stays only inside B. Robotics software, flagged. |
| Image segmentation and classification / Feature extraction / Classical image processing (OpenCV) | Consolidated | C. Image segmentation and feature extraction. |
| Object detection (YOLOv11) | Retained | C. Object detection (HYDRA). |
| Explainable AI | Retained, reworded | C. Model evaluation: Grad-CAM described as highlighting regions associated with a prediction. |
| Synthetic data generation | Removed | No evidence beyond the tool list. |
| Data annotation / CVAT / Roboflow / Label Studio | Consolidated | C. Data annotation and dataset preparation. |
| Python data stack | Consolidated | E. Databases and data handling; E. Programming. |
| Model serving | Retained | E. Model-serving applications. |
| Experiment tracking and reproducibility | Narrowed | E. Development workflow: only the fixed random seeds found in RETINA. |
| Model export and optimisation (ONNX, quantisation, TFLite) | Mostly removed | No evidence. TensorFlow Lite kept inside A. Connected devices, flagged. |
| Data pipelines | Consolidated | C. Data annotation and dataset preparation. |
| Microcontroller programming / Microprocessor platforms | Consolidated | A. Microcontroller and single-board computer platforms. |
| Pulse oximetry, gas, motion, environmental, distance, camera sensors | Consolidated | A. Sensor integration. Only MAX30102, cameras and alcohol sensing have project evidence. |
| Serial and bus interfaces | Retained | A. Firmware and hardware interfaces. |
| IoT and connected prototypes / Edge AI and TinyML | Consolidated, flagged | A. Connected devices and edge processing. |
| Gazebo with ROS 2 / NVIDIA Isaac Sim / CoppeliaSim / Webots | Consolidated, flagged | B. Robotics software and simulation, grouped by purpose. |
| Robot and automation control | Reworded | B. Control logic and automated operating sequences. Industrial automation training (PLC, SCADA, industrial robots) is a separate capability, flagged. |
| Sensor and actuator integration / System integration and testing / Robotics mentoring | Retained | B. |
| CAD | Retained, flagged | D. Enclosure and mechanical design. No software named and no project link. |
| LTspice / Logisim Evolution / NI Multisim | Consolidated | D. Analog and digital circuit simulation. |
| Proteus VSM / Wokwi / Tinkercad / SimulIDE / Renode / PICsimLab | Consolidated, flagged | D. Microcontroller and firmware simulation. |
| Python / C and C++ / MATLAB / JavaScript / SQL | Consolidated | E. Programming. |
| Bash and PowerShell | Moved | E. Development workflow. |
| HTML5, CSS3 and responsive design / JavaScript UI logic / Charts and dashboards / Model-output interfaces / Interactive maps | Consolidated | E. Engineering interfaces and reports. |
| Streamlit and Gradio / React and TypeScript / Tailwind CSS | Consolidated, flagged | E. Rapid demos and front-end frameworks. |
| Next.js / Vite / Progressive web apps | Removed | No evidence and low relevance to the target roles. |
| Plotly and Chart.js | Removed | Matplotlib and Leaflet are the charting tools with evidence. |
| 3D visualisation | Removed from skills | HYSEIS still mentions interactive 3D visualisation on its project page. |
| Browser camera access / Accessibility and performance | Removed | No project evidence. |
| API integration / REST APIs | Replaced | E. Model-serving applications now says 'HTTP routes', which the RETINA source confirms. |
| Flask | Retained | E. Model-serving applications. |
| SQLite and relational databases / NumPy, Pandas and Matplotlib | Consolidated, flagged | E. Databases and data handling and E. Engineering interfaces. pandas is not used in RETINA. |
| PDF and report generation | Retained | E. Engineering interfaces and reports (ReportLab in RETINA). |
| Git and GitHub / Jupyter and VS Code | Consolidated, flagged | E. Development workflow. |
| Mathematical modelling / Seismic statistics | Consolidated | F. Mathematical modelling and numerical analysis. |
| Research design / Statistical analysis | Retained, made specific | F. Statistical analysis and research design (Pearson/Spearman, z-score standardisation, ROC / Youden's J). |
| Technical documentation | Retained | F. Technical documentation and communication. |
