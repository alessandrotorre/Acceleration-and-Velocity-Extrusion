#Name: Export to LinuxCNC Velocity Extrusion
#Info: Adapted GCode to Acceleration and velocity Extrusion based 3D printer
#Depend: GCode
#Type: postprocess
#Last modified Feburary 06/06, 2016
#Author Alessandro Torre alessandro.torrebo@gmail.com
import re


a=0
a_old=0
z_old=0
retraction=0
V_E_check=-1
A_in_line = -1
overextrude=overextrude_old=0

with open(filename, "r") as f:
	lines = f.readlines()
	lunghezza_r= len(lines)
	print lunghezza_r
with open(filename, "w") as w:
	# w.write(';M120 Pn.nn,   n.nn=layer_height [mm]\n')
	# w.write(';M150 unlink nozzle from XY\n')
	# w.write(';M151 link nozzle to XY\n')
	# w.write(';M130 retraction \n')
	# w.write(';M131 precharge\n')
	# w.write(';M180 Pnn.nn sets K extrusion acceleration factor related to X  Y accelerations \n')
	# w.write('(AXIS,stop)\n')
	# w.write('G64 P0.05 Q0.005\n')
	# w.write ('M111\n')
	for line in lines:
		if "G92" in line: 
			line = ""
			w.write (line)
		elif ";" in line:
			#line = ""
			w.write(line)
			if(";TYPE:FILL" in line):
				overextrude=1
			elif(";TYPE:WALL-INNER" in line):
				overextrude=0
			elif(";TYPE:WALL-OUTER" in line):
				overextrude=0
			elif(";TYPE:SKIN" in line):
				overextrude=0
			elif(";LAYER" in line):
				overextrude=0
			elif(";TYPE:SUPPORT" in line):
				overextrude=0
			if ((overextrude!=overextrude_old) and (overextrude==1)):
				Altezza_layer_fill=Altezza_layer*1.9
				w.write ('M120 P%1.2f\n' %Altezza_layer_fill)
			elif ((overextrude!=overextrude_old) and (overextrude==0)):
				w.write ('M120 P%1.2f\n' %Altezza_layer)
			overextrude_old=overextrude
		else:
			valori = line.split(" ")		
			i=0	
			
			#w.write ('overextrude:'+str(overextrude)+'\n')
			if 1:
				#print(valori[0])
				i=0
				for i in range(len(valori)):
					if 'Z' == valori[i][0]:
						z = str(valori[i])
						z = float(z[1:]) 
						Altezza_layer=z-z_old
						z_old=z
						if ((Altezza_layer)>0):
							w.write ('M120 P%.2f\n' %Altezza_layer)
					if 'A' == str(valori[i][0]):
						A_in_line =1
						#print len(valori)
						a = str(valori[i]) 
						a = float(a[1:]) 
						valori[i] = ''  #A value will be deleted
						line = (" ".join(valori))+'\n'
						if (a<a_old):
							retraction=1
							w.write('M130\n')
							a_old=a
							V_E_check=0
						elif ((a>a_old) and (retraction==0)):
							if (V_E_check==0):
								w.write("M151\n")
								V_E_check=1
							a_old = a
						elif ((a>a_old) and (retraction==1)):
							retraction=0
							w.write('M131\nM151\n')  # M131 sets precharge and M151 links the nozzle to XY vel
							V_E_check=1
							a_old=a
						elif (a==a_old):
							if (V_E_check==1):
								w.write("M150\n")
								V_E_check=0
				if ( A_in_line != 1): # if A is not in line, the A axis will be unlink from XY velocity 
						if(V_E_check==1):
							w.write("M150\n")
							V_E_check=0
				A_in_line=-1
				w.write(line)
			elif "M84" in line:
				line = ""				
			elif "M107" in line:
				line = ""	
			#elif "M109" in line:
			#	line = ""			
			elif "T0" in line:
				line = ""
			else:
				w.write(line)
		
						
f.close()
w.close()
