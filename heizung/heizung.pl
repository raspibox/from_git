##########################################
# 	File:		heizung.pl
#	Date:		2012-12-17
#	Version:	0.4
#	History:0.2:Initial version 
#			0.3:	2012-12-15
#				-added function to log w1 meassure problems (meassures then -1.25°C)
#				-logfile output
#			0.4:	2012-12-17
#				-Email Notification wenn Heizstab aktiv oder Sammlertemp unterschritten
#			0.5:	2013-08-07
#				-Weitere OneWire Sensoren
#			0.6:	2013-09-18
#				-Solar und Abgastemperatur per python-Skript
#			0.7:	2014-09-08 
#				-Pfade für logfiles angepasst
#			0.8:	2015-08-25
#				-Alte Verweise auf Volkszaehler entfernt
##########################################


use warnings;
use lib "/eiler";
use eiler;

#			Arduino				Raspi
# Address: 103398290208001C  10-000802299833	(= 1 Ring)
# Address: 10F59DE2010800AA  10-000801e29df5	(= 2 Ringe)
# Address: 103C1AFA0108001D  10-000801fa1a3c	(= 3 Ringe)
# Address: 10FE9E2902080055  10-000802299efe	(= 4 Ringe)
# Address: 10D58D2902080029  10-000802298dd5	(= 5 Ringe)	KESSELTEMP
# Address: 1085712902080080	 10-000802297185	(= 6 Ringe)	SOLAR_RL 
# Address: 10889029020800DD  10-000802299088	(= Kennzeichnung "VII")
# Address: 107D605B020800DD 				(= Kennzeichnung "VIII") 


my $i2c_read_device = 0x3e;	#I2C Adresse des Bausteins

#define and open logfiles for logging
my $errLog = "/var/log/heizung_2_error.log";
my $stdLog = "/var/log/heizung_2.log";
open (ERR, ">>$errLog") || die "Can not open file $errLog: $!";
open (LOG, ">>$stdLog") || die "Can not open file $stdLog: $!"; 

$solar=25; #Global Solar Kollektor Temperatur

#Set Autoflush-Flag to "1" to enable direct writing to filehandle
$old_fh = select(LOG);
$| = 1;
select($old_fh);

$old_fh = select(ERR);
$| = 1;
select($old_fh);
 
# aussen 7e9b8a70-37a0-11e4-b8b1-7dbd4d4a8024

my %aTempSensoren = (
	"P1" 		=>	"/sys/devices/w1_bus_master1/10-000802299833/w1_slave",
	"P2"		=>	"/sys/devices/w1_bus_master1/10-000801e29df5/w1_slave",	
	"P3"		=>	"/sys/devices/w1_bus_master1/10-000801fa1a3c/w1_slave",	
	"P4"		=>	"/sys/devices/w1_bus_master1/10-000802299efe/w1_slave",	
	"Kessel"	=>	"/sys/devices/w1_bus_master1/10-000802298dd5/w1_slave",	
        "Solar_RL"      =>      "/sys/devices/w1_bus_master1/10-0008025feaf3/w1_slave",
        "Solar_VL"      =>      "/sys/devices/w1_bus_master1/10-0008025fd3d5/w1_slave",
        "Aussen"        =>      "/sys/devices/w1_bus_master1/10-000802299088/w1_slave",
        "KWL_Ansaug"    =>      "/sys/devices/w1_bus_master1/10-0008025fd3d5/w1_slave",
        "KWL_Abluft"    =>      "/sys/devices/w1_bus_master1/10-0008025fd3d5/w1_slave",
        "KWL_RaumZuluft"      =>      "/sys/devices/w1_bus_master1/10-0008025fd3d5/w1_slave",
        "KWL_RaumAbluft"      =>      "/sys/devices/w1_bus_master1/10-0008025fd3d5/w1_slave",
 );

my %aSensorenUUID = (
	"P1" 		=>	"f90d90c0-3855-11e4-8db8-dde4f9d55054",
	"P2"		=>	"1b078e70-3856-11e4-97ed-8b65a8b6f493",	
	"P3"		=>	"4ebd38b0-3856-11e4-a388-7dd33cbbdbf2",	
	"P4"		=>	"7137d420-3856-11e4-94ff-37311e044172",	
	"Kessel"	=>	"97fa8800-3856-11e4-becd-31bf596eab94",	
        "Solar_RL"      =>      "e3995660-3856-11e4-87b8-2baccf27489f",
        "Solar_VL"      =>      "c2e9f560-3856-11e4-84d9-e5c21eaca6a1",
        "Aussen"        =>      "7e9b8a70-37a0-11e4-b8b1-7dbd4d4a8024",
        "Abgas"         =>      "2aef8120-3857-11e4-b18c-7de805a4de63",
        "Kollektor"     =>      "48776b50-3857-11e4-a15d-4f05111795d2",
	"Ventil"	=>	"c69a2fe0-3860-11e4-97d1-e9f63cc6131e",
 );






#check if I'm not on the pi. Because on not raspi there is no i2c, w1, ... working. These function calls must then be excluded from execution.
$hostname = `hostname`;
chomp($hostname);
if ($hostname eq "raffa-acer"){
	print "hostname: $hostname\n";
	$debug = 1;
	&wlf("debug = 1 as hostname = $hostname");
}


#&wlf("##############################################################################");
#&wlf("########### Started on host: $hostname");
 


sub wlf {  #write log file
	my $text=$_[0];
	print LOG (&getTimeStamp)." $text \n";	
	print LOG " $text \n";	
}

sub welf {  #write error log file
	my $text=$_[0];
	print ERR (&getTimeStamp)." $text \n";	
}

sub getTempValue {	#read content of file to get temperature
	if ($debug) {return "88.8"}; 
	my $sSensor = $_[0];
	my $sSensorfile= $aTempSensoren{"$sSensor"};
	my $sUUID= $aSensorenUUID{"$sSensor"};
 
	#print "### Open File: $sSensorfile\n";
	&wlf("Open File: $sSensorfile");
	open IN, "$sSensorfile"	or warn "Fehler: $!";
		while (<IN>){
			#print $_;
			if (/NO/){
				#print "### Checksumme falsch\n";
				&welf("Checksum wrong from file $sSensorfile");
				return "";
			}
			if (/.*t=(.*)/){
				my $Wert= $1;
				$GradC = $Wert/1000;
				if ($GradC == -1.25){
					#print "$sSensor hat -1.25 Grad angezeigt\n";
					&welf("Sensor $sSensor hat -1.25 Grad angezeigt. Wert wird verworfen");
					return "";
				}elsif($GradC == 85){
					#print "$sSensor hat 85 Grad angezeigt\n";
					&welf("Sensor $sSensor hat 85 Grad angezeigt. Wert wird verworfen");
					return "";
				}else{ 
					#print "### Sensor $sSensor hat $GradC Grad C.\n";
					&wlf("Sensor $sSensor ($sSensorfile) has $GradC Grad C.")
				}
			}
		}
	#$ret = `curl -d "" "http://10.0.0.50/middleware.php/data/$sUUID.json?value=$GradC" >/dev/nul`;
	return "$GradC";
}

sub getAnalogAbgas {
#	$abgas = `python /eiler/analog.py abgas`;
	$abgas = `python /home/pi/from_git/heizung/analog.py abgas`;
	chomp $abgas;
	return $abgas;
}

sub getAnalogSolar {
	#print "Durchlauf: $i\n";
	if ($i % 10 == 1){	#Messung der Kollektortemp nur bei jeder x-ten Messung, da dies den Messert der WOLF Steuerung beeinflusst wenn das Signal zu oft fehlt
		#print "Treffer: $i\n";
		$solar = `python /home/pi/from_git/heizung/analog.py solar`;
		chomp $solar;
		#print "http://10.0.0.50/middleware.php/data/$aSensorenUUID{\"Kollektor\"}.json?value=$solar";
		#$ret = `curl -d "" "http://10.0.0.50/middleware.php/data/$aSensorenUUID{"Kollektor"}.json?value=$solar"`;
		#$ret = `curl -d "" "http://10.0.0.50/middleware.php/data/$aSensorenUUID{"Ventil"}.json?value=1"`;
		return $solar;
	}else{
		#$ret = `curl -d "" "http://10.0.0.50/middleware.php/data/$aSensorenUUID{"Ventil"}.json?value=0"`;
		return $solar;
	}
}



$i=1;
while ( $i ){
	lese_i2c();
	
	sendeTemp();
	#print "### warten...\n";
	sleep(9); # Skriptausführung benötigt ca. 6s. Bei 9s Wartezeit kommt dann alle 15s ein Messwert in die DB
	$i++; # wir bauen hier mit Absicht eine Endlosschleife. Mit der $i kann man die Anzahl der Durchlaeufe zaehlen.
}

sub lese_i2c {
	my $channel = $_[0];
	
	#give all 
	$i2c_0 = 0.5; #init Channel 0 
	$i2c_1 = 1; #init Channel 1 
	$i2c_2 = 1.5; #init Channel 2 
	$i2c_3 = 2; #init Channel 3 
	$i2c_4 = 2.5; #init Channel 4
	$i2c_5 = 3; #init Channel 5 
	$i2c_6 = 3.5; #init Channel 6 
	$i2c_7 = 4; #init Channel 7 
	my $ret;
	if (not $debug) {
		$ret = `i2cget -y 1 $i2c_read_device`;
		&wlf("Return from i2c device with adress $i2c_read_device: \"$ret\"");
	}else{
		$ret = 0xff;  #dummy value when not running on a raspi
	};
	#print "ret: $ret\n";
	my $number = hex($ret);
	#print "num: $number\n";
	my $dec = $number;
	#print "dec: $dec\n";
	
	my @bits;
	$bits[7] = ($dec & 128) <=> 0;
	$bits[6] = ($dec & 64) <=> 0;
	$bits[5] = ($dec & 32) <=> 0;
	$bits[4] = ($dec & 16) <=> 0;
	$bits[3] = ($dec & 8) <=> 0;
	$bits[2] = ($dec & 4) <=> 0;
	$bits[1] = ($dec & 2) <=> 0;
	$bits[0] = ($dec & 1) <=> 0;
	
	$bin_read_i2c_values = join '', reverse @bits;
	#print "### $bin_read_i2c_values\n";
	#printf "The entered decimal number in binary is : %s\n", join '', reverse @bits;
	$i2c_0 += 10 if ($bits[0] == 0);
	$i2c_1 += 10 if ($bits[1] == 0);
	$i2c_2 += 10 if ($bits[2] == 0);
	$i2c_3 += 10 if ($bits[3] == 0);
	$i2c_4 += 10 if ($bits[4] == 0);
	$i2c_5 += 10 if ($bits[5] == 0);
	$i2c_6 += 10 if ($bits[6] == 0);
	$i2c_7 += 10 if ($bits[7] == 0);
	#return $bits[$channel];
	}

sub sendeTemp {
	#$sHTTPGetStringParameter="TEMP_ABGAS=1&TEMP_SOLAR_KOLLEKTOR=0&TEMP_UNDEF=0&STAT_KESSEL_PUMPE=".$i2c_0."&STAT_ABGAS_LUEFTER=".$i2c_1."&STAT_SOLAR_PUMPE=".$i2c_2."&STAT_HEIZSTAB=$i2c_3&key=raffa";
	&wlf("collect all data before sending");
	$sHTTPGetStringParameter="t_AUSSEN=".getTempValue("Aussen")."&t_P1=".getTempValue("P1")."&t_P2=".getTempValue("P2")."&t_P3=".getTempValue("P3").
		"&t_P4=".getTempValue("P4")."&t_SOL_RL=".getTempValue("Solar_RL")."&t_SOL_VL=".getTempValue("Solar_VL")."&t_ABGAS=".getAnalogAbgas.
		"&t_KESSEL=".getTempValue("Kessel")."&t_SOL_KOLL=".getAnalogSolar."&t_UNDEF=0&s_KES_PUMPE=".$i2c_0."&s_LUEFTER=".$i2c_1."&s_SOL_PUMPE=".$i2c_2."&s_HEIZSTAB=".$i2c_3.
		"&s_GARAGE=".$i2c_4."&key=raffa";
	#print "### Writung data to http://ertest.bplaced.net/push_data.php\n";
	#print "### Parameter: $sHTTPGetStringParameter\n";
	$sURL= "curl \"http://ertest.bplaced.net/push_data.php?$sHTTPGetStringParameter\"";
	&wlf ("Sending request: $sURL\n");
	if (not $debug) {$ret = `curl "http://ertest.bplaced.net/push_data.php?$sHTTPGetStringParameter"`};
	$sHTTPGetStringParameter=getTempValue("Aussen");
	my $CurlParam = "curl -X PUT -H \"Content-Type: text/plain\" http://sd-defekt:8080/rest/items/Temp_Brauchwasser/state -d " . getTempValue("P4") ;
	print "$CurlParam\n";	
	if (not $debug) {$ret = `$CurlParam`};
	print "ret: $ret\n";        
	#print "para: $sHTTPGetStringParameter\n";
	#&wlf ("Sending request to VZ");
    #    if (not $debug) {$ret = `curl -d "" "http://10.0.0.50/middleware.php/data/7e9b8a70-37a0-11e4-b8b1-7dbd4d4a8024.json?value=$sHTTPGetStringParameter"`};
        #print "ret: $ret\n";
#        &wlf ("Sending request to testserver:\n");
#        if (not $debug) {$ret = `curl "http://10.0.0.54/push_data.php?$sHTTPGetStringParameter"`};
#        print "ret: $ret\n";
 
}
