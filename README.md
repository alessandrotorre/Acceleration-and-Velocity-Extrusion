# Acceleration-and-Velocity-Extrusion

This is a step by step guide  to test the version of Acceleration and Velocity of extrusion. 
Here, there is everything you need to test it.

- A glade widget that can be added to yours GUI - gmoccapy or axis. 
- the hal file with nettings "from and to" the component and the GUI.
- the M codes 
- the postprocessor for cura

1. setup a config with gmoccapy or axis as GUI
2. create your MCODE path ( Ex. mkdir /home/machinekit/machinekit/MCODE)
3. add that path in the [RS274NGC] section of your ini file ( Ex. USER_M_PATH = home/machinekit/machinekit/MCODE ) 
4. put all the Mcodes in your MCODE path 
5. give permissions to the path ( sudo chmod +x -R /home/machinekit/machinekit/MCODE )
6. install machinekit-dev 
   sudo apt-get install machinekit-dev
7. Install the components. In the pattern where you extracted the .comp, write:
sudo halcompile --install VelocityExtrusion.comp
sudo halcompile --install orLastVariation.comp

8. in the [DISPLAY] section of your ini file
add
>EMBED_TAB_NAME=Acceleration and Velocity of Extrusion
>EMBED_TAB_LOCATION = ntb_preview
>EMBED_TAB_COMMAND= gladevcp -x {XID} -H AccVelExtr.hal ./guiAccVelExtr.ui
9. put the guiVelExtr.ui and AccVelExtr.hal files in the same folder of your .ini file and give the execution permission to both 
10. add the postprocessor for CURA in the cura plugin folder.

11. In the machine settings of CURA, chose Gcode flavor Mach3/linuxCNC 
12. Assign a very high value to the FERROR and MIN_FERROR in the [AXIS_4] section in yours .ini file

Hints:
In VE_cura_postprocessor.py I used an infill volume of 1.9 instead of 1, because the slicer makes the lines pattern in a crossed way of 90° between layers and it generates infill without floor. If you want you can change that parameter at line 56 of VE_cura_linuxcnc.py

Mcodes: 
It is easier for me remember the command that ends with "1" like 111, 131 or 151 as "ON" status and the ones that ends with "0" like 110,130 or 150 as "off" status.

Mcodes leggends: 
- M110 switch to normal mode, not Velocity Extrusion
- M111 switch to Velocity Extrusion mode
- M120 Pxx.xx: sets the layer height
- M130 do a retraction of xx mm at at velocity specificated in the GUI
- M131 do a precharge of xx mm at Velocity specificated in the GUI
- M135 Pxx.xx: sets the Nozzle diameter
- M150 unlink the nozzle
- M151 link the nozzle

Todo
- improve the preventive homing of the A axis and g92 A0: there are problems when you Turn on and off the component with M110 and M111, because the value of the VelocityExtruder.0.A and axis.3.motor-pos can be different. 
For example if the relative position, with velocity extrusion mode ON, was 1000mm and the axis.motor-pos is 85mm, when you do a M110 is like to command a movement of 1000-85=-915 mm to the A axis.
- fix the bugs of the postprocessor
- fix the MCODES: if pin "Velocity.Extrusion.0.isenbaled != TRUE" you can't command MCODE as M130 M131 M150 or M151. I'm able to display a warning message in the stderr display, but not yet in the GUI. Do you know a way to call rtapi_print_msg(RTAPI_MSG_ERR, " ..........") from bash or from MCODE?
