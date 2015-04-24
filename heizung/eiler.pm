#!/usr/bin/perl 
##########################################
# 	File:		eiler.pm
#	Date:		2012-12-15
#	Version:	0.1
#	History:	Initial version
##########################################
#use strict;
use warnings;
use Time::Local;




sub getTimeStamp (){   #returns: "2012-12-14 22:29:58"
	my ($Sec, $Min, $Hour, $Day, $Month, $Year, $DayOfWeek, $DayOfYear, $DST) = localtime(time);
	$Year += 1900;
	$Month += 1;
	$Sec = '0'.$Sec if $Sec<10;
	$Min = '0'.$Min if $Min<10;
	$Hour = '0'.$Hour if $Hour<10;
	$Day = '0'.$Day if $Day<10;
	$Month = '0'.$Month if $Month<10;
	
	#my $sTimeStamp = "2012-12-14 22:29:58";
	my $sTimeStamp = "$Year-$Month-$Day $Hour:$Min:$Sec";
	#print "$sTimeStamp\n";
	return($sTimeStamp);
	}



sub getTimeStampFS (){	#returns: "2012-12-14_23h23m34"
	
	my ($Sec, $Min, $Hour, $Day, $Month, $Year, $DayOfWeek, $DayOfYear, $DST) = localtime(time);
	$Year += 1900;
	$Month += 1;
	$Sec = '0'.$Sec if $Sec<10;
	$Min = '0'.$Min if $Min<10;
	$Hour = '0'.$Hour if $Hour<10;
	$Day = '0'.$Day if $Day<10;
	$Month = '0'.$Month if $Month<10;
	
	#my $sTimeStamp = "2012-12-14 22:29:58";
	my $sTimeStampFS = "$Year-$Month-$Day"."_$Hour"."h$Min"."m$Sec";
	#print "$sTimeStampFS\n";
	return ($sTimeStampFS);
	}


1;
