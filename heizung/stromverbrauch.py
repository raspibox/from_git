#!/usr/bin/python3
import os
import subprocess
from datetime import datetime
import time
import sys

# Check if parameter 1 (Debug level) is set 
if len(sys.argv) >= 2:
	dbg_level = int(sys.argv[1])
else:
	# Set debug level to no output
	dbg_level = 0
	



#get the number of loops
loop_counter = 0

# Send Zaehlerstand only every X loop
loop_modulo = 20

# Definition of our "Start String". This String indicates the OBIS ID 1.8.0
Suchstring_Zaehlerstand = "070100010800FF"
Suchstring_AktuelleLeistung ="770701000F0700FF0101621B520065"
# Get data from IR data receiver (see Volkszaehler "USB IR Lesekopf")
# Retuns a string like this (all in one line) 
# "b'1B1B1B1B0101010176050C9438CA620062007263010176010105043168440B0649534B01027A20DE0E01016366360076050C9438CB620062007263070177010B0649534B01027A20DE0E070100620A
# FFFF726201650726763D7777078181C78203FF010101010449534B0177070100000009FF010101010B0649534B01027A20DE0E0177070100010800FF650000018201621E52FF590000000006858C530177070100010801FF0101621E52FF
# 590000000006858C530177070100010802FF0101621E52FF59000000000000000001770701000F0700FF0101621B52006500000A390177078181C78205FF010101018302A06F12BD3C0D6DDD2D64BC6D98F18FC2D3D6C5B2B3F29D402E7
# B7C5DF4A76CA3405184477DEB455A9E8F74F7D4D1B03F01010163AB250076050C9438CC62006200726302017101636207001B1B1B1B1A006\n'"

# Configure serial device
returncode = subprocess.check_output('/bin/stty -F /dev/ttyUSB0 1:0:8bd:0:3:1c:7f:15:4:5:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0', shell=True)



true = 1
while true:
	# increment loop_counter
	loop_counter = loop_counter + 1
	# Get data from serial device
	sml_message = str(subprocess.check_output('cat /dev/ttyUSB0 2>/dev/null | xxd -p -u -l 324 -c 324', shell=True))
	if dbg_level == 2: print (sml_message)
	
	
	# Find start position of OBIS 1.8.0 
	Position_Zaehlerstand = sml_message.find(Suchstring_Zaehlerstand)
	
	# ####################################################################
	# Find start position of OBIS xx 
	Position_AktuelleLeistung = sml_message.find(Suchstring_AktuelleLeistung)
	if Position_AktuelleLeistung < 0:
		print("String AktuelleLeistung konnte nicht gefunden werden")
		continue
	
	if dbg_level == 2: print ("Position_AktuelleLeistung: ",Position_AktuelleLeistung)
	# After we found start position we cut out requested data
	Substring_AktuelleLeistung = sml_message[Position_AktuelleLeistung+30:Position_AktuelleLeistung+38]
	#print (Substring_AktuelleLeistung)
	
	# Check if returened date has expected size of 8 char.
	if len(Substring_AktuelleLeistung) < 8:
		print("Something was wrong. Date not long enough!")
		continue
	
	
	if "\\" in Substring_AktuelleLeistung:
		print("String contains EOL char. Skipping.", Substring_AktuelleLeistung)
		continue
	
	
	#Convert Hex data to a integer
	Watt = int(Substring_AktuelleLeistung,16) 
	if dbg_level: print ("Aktuelle Abnahme in Watt: ", Watt)
	
	Watt_String = str(Watt)
	cmd = 'curl -X PUT -H "Content-Type: text/plain" -d ' + Watt_String + ' "http://sd-defekt:8080/rest/items/Electricity_Watt/state"'
	# print (cmd)
	os.system(cmd)
	
		
	# get Zaehlerstand only every X loops
	if loop_counter % loop_modulo == 0 :
			# After we found start position we cut out requested data
		Substring_Zaehlerstand = sml_message[Position_Zaehlerstand+36:Position_Zaehlerstand+52]
		if dbg_level == 2: print (Substring_Zaehlerstand)
		#print (len(Substring_Zaehlerstand))
		
		# Check if returened date has expected size of 16 char.
		if len(Substring_Zaehlerstand) < 16:
			print("Something was wrong. Data not long enough!")
			continue
		
		if "\\" in Substring_Zaehlerstand:
			print("String contains EOL char. Skipping.", Substring_Zaehlerstand)
			continue
		
		
		# Convert extract into a int
		ZaehlerstandExtraxt_Int = int(Substring_Zaehlerstand,16)
		#print ("2:", ZaehlerstandExtraxt_Int)
		
		
	
		
		KWh_Float = float(ZaehlerstandExtraxt_Int / 10000.0)
		if dbg_level: print ("Zaehlerstand in KWh", KWh_Float)
		
		#Convert to a string as otherwise curl wont work
		KWh_String = str(KWh_Float)
		#print (KWh_String)
		
		cmd = 'curl -X PUT -H "Content-Type: text/plain" -d ' + KWh_String + ' "http://sd-defekt:8080/rest/items/Electricity_KWh/state"'
		# print (cmd)
		os.system(cmd)
		#time.sleep(5)
	
	
