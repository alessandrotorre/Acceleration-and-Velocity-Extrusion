# Acceleration-and-Velocity-Extrusion

This is a guide step by step to test version of Acceleration and Velocity extrusion. 
Here, there is everything u need to test it.

- a glade widget that can be added to yours GUI - gmoccapy or axis. 
- the hal file with nettings "from and to" the component and the GUI.
- the M codes 
- the postprocessor for cura

1) setup a config with gmoccapy or axis as GUI
2) create your MCODE path ( Ex. mkdir /home/machinekit/machinekit/MCODE)
3) add that path in the [RS274NGC] section of your ini file ( Ex. USER_M_PATH = home/machinekit/machinekit/MCODE ) 
4) puts all the Mcodes in your MCODE path 
5) give permissions to the path ( sudo chmod +x -R /home/machinekit/machinekit/MCODE )
6) install machinekit-dev 
- sudo apt-get install machinekit-dev
7) Install the components. In the pattern where you extracted the .comp, write:
sudo halcompile --install VelocityExtrusion.comp
sudo halcompile --install orLastVariation.comp

8) in the [DISPLAY] section of your ini file
add
EMBED_TAB_NAME=3D Printing I5D
#IF GMOCAPPY decomment the next line
#EMBED_TAB_LOCATION = box_coolant_and_spindle  
EMBED_TAB_LOCATION = ntb_preview
EMBED_TAB_COMMAND= gladevcp -x {XID} -H VelExtr.hal ./guiVelExtr.ui

9)add the postprocessor for the CURA in the cura plugin folder. 
In VE_cura_postprocessor I used an infill of 1.9 instead of 1, because cross the section at 45 or -45 was wrong in my opinion. If u want you can change that parameter at line
this is the most incomplete solution
To try it u need to install python in ur pc

10)I used a mach3/linuxcnc config in cura

I didn't use the same Mcode of Bas. 
It was easier for me remember the command that ended with "1" like 111 or 151 as "ON" status and with "0" as "off" status.


M110 switch to normal mode, not Velocity Extrusion
M111 switch to Velocity Extrusion mode
M120 Pxx.xx: sets the layer height
M130 do a retraction of xx mm at velocity specificated in the GUI
M131 do a precharge of xx mm at Velocity specificated in the GUI
M135 Pxx.xx: sets the Nozzle diameter
M150 unlink the nozzle
M151 link the nozzle

Todo
- improve the preventive homing of the A axis and g92 A0
- fix the bugs of the postprocessor
