# Optical Switch Evaluation Program
---
This program serves as a simple, but hopefully expandable, tool for evualating the power attenuation of opticals switches. It is deisgned to be connected to an optical power meter and one optical switch.

## Structure
This program is structured to allow for easy expansion and modification. That structure is as follows:

```
Optical-Switch-Eval/
├── app/
|   ├── controllers/
|   |   ├── __init__.py
|   |   └── main_controller.py
|   ├── models/
|   |   ├── __init__.py
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
└── ReadMe.md
```

### controllers
Controllers contains the main controller, which bridges the gap between the GUI and the logic. main_controller.py should only take inputs from the GUI and pass them along to the model. 

### models
Models contains all the logic related components of the program. evaluation_model contains the opm and optical switch objects and is responsible for interacting with them.

### viewers
Viewers contains all GUI elements. It is simply responsible for displaying elements of the GUI and defining and GUI only interactions.

### X2OOptics
X2OOptics is a psuedo-custom package for the program which contains the classes needed for interacting with the hardware. Only 2 files are currently used in the program but the additional files are included for future use, if needed.

## Operation
Upon startup the user will ahve to enter a connection path for the OPM and the optical switch. Once this is done a label must be provided and then collection of power can begin. When switching to different channels there is a hardware delay as the channel is physical switched, during this time the GUI is disabled to prevent any hardware errors due to bad user interaction. Once all data is collected, the "save data" button will save the collected data to a csv file named **optical_switch_powers_YYYYMMDD_HHMMSS.csv**, under Optical-Switch-Eval.