# Optical Switch Evaluation Program
---
This program serves as a simple, but hopefully expandable, tool for evaluating the power attenuation of opticals switches. It is designed to be connected to an optical power meter and one optical switch.

## Operation
Upon startup the user will have to enter a connection path for the OPM and the optical switch. Once this is done a label must be provided and then collection of power can begin. When switching to different channels there is a hardware delay as the channel is physical switched, during this time the GUI is disabled to prevent any hardware errors due to bad user interaction. Once all data is collected, the "save data" button will save the collected data to a csv file named **optical_switch_powers_YYYYMMDD_HHMMSS.csv**, under Optical-Switch-Eval.