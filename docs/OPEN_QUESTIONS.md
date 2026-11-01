# Open questions and unresolved information

Please answer these before you share the link. Items marked **blocking** affect what is public now.

## Decisions that change what is public
1. **Résumé PDF contents (blocking).** The résumé you supplied contains your phone number and both PRC licence numbers. The site's HTML pages omit them, but the downloadable PDF shows them. Publish as is, or provide a public version with those lines removed?
2. **Videos now published (blocking).** At your request all five videos are on the site. Two carry risk: the *school system* recording appears to show learner and staff records and a staff photo, and the *Smart Helmet news feature* is a One News broadcast with identifiable students. Confirm you have the right and consent to publish both. To hide one, set `"publish": false` in `content/media.json`, then rerun `optimize_media.py` and `build.py`.
3. **Press images not used.** `Image 4.jpg` (DOST post) and `image 6.png` (ABS-CBN) belong to those organisations and show identifiable people. I cited the coverage in text only. Send URLs if you want clickable references.
4. **Phone, LinkedIn, GitHub.** The résumé has no LinkedIn or GitHub, and I did not publish your phone number. Tell me the URLs (and whether to show the phone) and I will add them.

## Your role (please confirm each; wording is deliberately cautious until then)
| Project | Currently published | What I need |
|---|---|---|
| Smart Helmet | "Mentor of the student team" (inferred from résumé + news credit) | Your actual tasks (design review, testing, coaching), and who built what. |
| RETINA | "Researcher and developer" (inferred from the code and the RetinaMFA draft in your working folder) | Confirm authorship; confirm the draft may be described publicly; is it final or a draft? |
| HYDRA, HYSEIS, SAFARIS | "Project author", contribution not itemised | Your specific work (hardware, models, interface) and any collaborators. |
| VISION, MATLAB project, School system | "Developer" (first person in your descriptions) | Anything to add, for example supervisors or teammates. |

## Missing evidence (the supplied "papers" contain none of this)
The brief asks for dataset sizes, splits, accuracy/precision/recall/F1/ROC-AUC/Dice/IoU, trial counts, response times, power, calibration, and failure cases. **None appear in any supplied document**, so none are published. Each case-study states this plainly. If you have results, send the numbers with their test conditions and I will add Testing and Results sections:
- HYDRA: dataset size, class labels, SVM accuracy or similar, how hydration was determined.
- HYSEIS: forecast evaluation versus observed aftershocks, data source and period, the fault dataset status.
- VISION / MATLAB project: datasets, splits, final accuracy, which of lung/brain/skin were trained.
- SAFARIS: model type, data source, accuracy, any field trial.
- RETINA: image count, healthy/abnormal split, statistics reported in the study.
- Smart Helmet: sensors and controller used, detection thresholds, test results.
- School system: stack, deployment status, any measured benefit.

## Other gaps
- **Years.** Only Smart Helmet has a date (2024). The Year filter and "Newest first" sort are built but switch on automatically once two or more projects have a `year`.
- **No robotics or microcontroller project.** The résumé lists robotics, embedded systems and IoT, but no supplied project documents a robot, microcontroller or protocol. The Skills page says so. If you have one, add it.
- **Skin-project screenshot provenance.** It looks like a captioned image from a web page. Confirm it is your own capture.
- **Thumbnails are illustrations.** They are labelled "Illustration". Prototype photographs exist only for the Smart Helmet. Add real screenshots or photos for others if you have them.
- **RetinaMFA.docx** is summarised, not hosted. Say so if you want it downloadable as a PDF.
- **Custom domain** and **public URL**: not yet created (see README, Deployment).
