#!/usr/bin/perl 
use strict; 
use Net::PcapUtils; 
use Win32::NetPacket 'GetAdapterNames', 'GetNetInfo' ; 
my $start; 
my $end; 
 
foreach ( GetAdapterNames() ) { 
        my ($ip, $mask) = GetNetInfo( $_ ); 
        if (($ip =~ /.+/) gt 0) { 
		my $error = Net::PcapUtils::loop(\&print_packet, DEV => $_); 
				} 
} 
 
sub print_packet { 
 
my($user_data, $header, $packet) = @_; 
 
if (index($packet,"HTTP") gt 0){ 
 
if ($packet=~/GET.+\/.+HTTP*/ gt 0 && !($packet=~/GET.+\/.+\.(gif|jpg|jpeg|css|js|png|swf|xml|ico).+HTTP*/ gt 0)) { 
		$start = (index($packet,"GET")); 
		$end = length($packet); 
		print substr ($packet, $start,($end-$start))."\n"; 
} elsif ($packet=~/POST.+\/.+HTTP*/ gt 0) { 
		$start = (index($packet,"POST")); 
		$end = length($packet); 
		print substr ($packet, $start,($end-$start))."\n"; 
} else { 
# Nothing interesting in packet :) 
} 
} 
} 
