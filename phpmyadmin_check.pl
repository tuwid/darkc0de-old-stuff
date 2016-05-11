#!/usr/bin/perl 
# phpMyAdmin Checker
# Author: cha0x <cha0x@darkc0de.com>
#
# thanks to: trxtxx (for the paths)

use strict;
use warnings;
use LWP::UserAgent;
use HTTP::Request;

my ($add,$iplist,$url,@path,@raw_data);

print q(
	
	phpMyAdmin Checker by cha0x
	   <cha0x@darkc0de.com>
	   	
);

if(@ARGV !=1) {
print "Usage: perl phpmyadmin.pl <IP/URL LIST> e.g. perl phpmyadmin.pl iplist.txt";
exit;
}

$iplist = shift;

@path = (
"/phpMyAdmin/",
"/PMA/",
"/admin/",
"/dbadmin/",
"/mysql/",
"/myadmin/",
"/phpmyadmin2/",
"/phpMyAdmin2/",
"/phpMyAdmin-2/",
"/php-my-admin/",
"/phpMyAdmin-2.2.3/",
"/phpMyAdmin-2.2.6/",
"/phpMyAdmin-2.5.1/",
"/phpMyAdmin-2.5.4/",
"/phpMyAdmin-2.5.5-rc1/",
"/phpMyAdmin-2.5.5-rc2/",
"/phpMyAdmin-2.5.5/",
"/phpMyAdmin-2.5.5-pl1/",
"/phpMyAdmin-2.5.6-rc1/",
"/phpMyAdmin-2.5.6-rc2/",
"/phpMyAdmin-2.5.6/",
"/phpMyAdmin-2.5.7/",
"/phpMyAdmin-2.5.7-pl1/",
"/phpMyAdmin-2.6.0-alpha/",
"/phpMyAdmin-2.6.0-alpha2/",
"/phpMyAdmin-2.6.0-beta1/",
"/phpMyAdmin-2.6.0-beta2/",
"/phpMyAdmin-2.6.0-rc1/",
"/phpMyAdmin-2.6.0-rc2/",
"/phpMyAdmin-2.6.0-rc3/",
"/phpMyAdmin-2.6.0/",
"/phpMyAdmin-2.6.0-pl1/",
"/phpMyAdmin-2.6.0-pl2/",
"/phpMyAdmin-2.6.0-pl3/",
"/phpMyAdmin-2.6.1-rc1/",
"/phpMyAdmin-2.6.1-rc2/",
"/phpMyAdmin-2.6.1/",
"/phpMyAdmin-2.6.1-pl1/",
"/phpMyAdmin-2.6.1-pl2/",
"/phpMyAdmin-2.6.1-pl3/",
"/phpMyAdmin-2.6.2-rc1/",
"/phpMyAdmin-2.6.2-beta1/",
"/phpMyAdmin-2.6.2-rc1/",
"/phpMyAdmin-2.6.2/",
"/phpMyAdmin-2.6.2-pl1/",
"/phpMyAdmin-2.6.3/",
"/phpMyAdmin-2.6.3-rc1/",
"/phpMyAdmin-2.6.3/",
"/phpMyAdmin-2.6.3-pl1/",
"/phpMyAdmin-2.6.4-rc1/",
"/phpMyAdmin-2.6.4-pl1/",
"/phpMyAdmin-2.6.4-pl2/",
"/phpMyAdmin-2.6.4-pl3/",
"/phpMyAdmin-2.6.4-pl4/",
"/phpMyAdmin-2.6.4/",
"/phpMyAdmin-2.7.0-beta1/",
"/phpMyAdmin-2.7.0-rc1/",
"/phpMyAdmin-2.7.0-pl1/",
"/phpMyAdmin-2.7.0-pl2/",
"/phpMyAdmin-2.7.0/",
"/phpMyAdmin-2.8.0-beta1/",
"/phpMyAdmin-2.8.0-rc1/",
"/phpMyAdmin-2.8.0-rc2/",
"/phpMyAdmin-2.8.0/",
"/phpMyAdmin-2.8.0.1/",
"/phpMyAdmin-2.8.0.2/",
"/phpMyAdmin-2.8.0.3/",
"/phpMyAdmin-2.8.0.4/",
"/phpMyAdmin-2.8.1-rc1/",
"/phpMyAdmin-2.8.1/",
"/phpMyAdmin-2.8.2/",
"/sqlmanager/",
"/mysqlmanager/",
"/p/m/a/",
"/PMA2005/",
"/pma2005/",
"/phpmanager/",
"/php-myadmin/",
"/phpmy-admin/",
"/webadmin/",
"/sqlweb/",
"/websql/",
"/webdb/",
"/mysqladmin/",
"/mysql-admin/");

open(IPLIST, $iplist) || die "[x] Error: File not found\n";  
@raw_data=<IPLIST>;
close(IPLIST);

print "[i] Scan Started\n\n";

foreach $url (@raw_data)
{
	chomp($url);
	foreach $add (@path)
	{
		my $address = $url.$add;
		my $con = HTTP::Request->new(GET=>$address);
		my $useragent = LWP::UserAgent->new;
		my $f = $useragent->request($con);

		if($f->is_success && $f->status_line =~ /200/)
		{
			print "[!] Found: $address\n";	
			
			open (F,">>","found.txt");
			print F "$address\n";
			close(F);
		}
	}
}
