# Optical Switch Evaluation Program
---
## Structure
This program is structured with an MVC pattern(Model-Viewer-Controller).

```
Optical-Switch-Eval/
├── app/
|   ├── controllers/
|   |   ├── __init__.py
|   |   └── main_controller.py
|   ├── models/
|   |   ├── __init__.py
|   |   ├── background_model.py
|   |   └── evaluation_model.py
|   ├── viewers/
|   |   ├── __init__.py
|   |   └── main_window.py
|   └── X2OOptics
|       ├── __init__.py
|       ├── mock_opm.py
|       ├── mock_optical_switch.py
|       ├── opm.py
|       ├── optical_switch.py
|       └── other...
├── main.py
├── devices.csv
└── ReadMe.md
```

### controllers
Controllers contains the main controller, which bridges the gap between the GUI and the logic. `main_controller.py` should only take inputs from the GUI and pass them along to the model. 

### models
Models contains all the logic related components of the program. `evaluation_model.py` contains the opm and optical switch objects and is responsible for interacting with them. `background_model.py` contains the logic object responsible for handling backend operations not related to evaluation(e.g. managing lists of saved devices)

### viewers
Viewers contains all GUI elements. It is simply responsible for displaying elements of the GUI and defining and GUI only interactions.

### X2OOptics
X2OOptics is a psuedo-custom package for the program which contains the classes needed for interacting with the hardware. Only 2 files are currently used in the program but the additional files are included for future use, if needed.