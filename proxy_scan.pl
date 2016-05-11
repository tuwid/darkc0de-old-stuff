#!/usr/bin/perl -w

######################################################################
# proxyScan v0.1
#
# by Ed Blanchfield http://www.e-things.org/
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Perl Artistic License or the
# GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any
# later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# If you do not have a copy of the GNU General Public License write to
# the Free Software Foundation, Inc., 675 Mass Ave, Cambridge,
# MA 02139, USA.
# 
# 
#######################################################################


use Getopt::Long;
use LWP::UserAgent;
use strict;

my $DEBUG;
my $ports;
my $targets;
my $proxy;
my $method;
my $delay;
my $timeout;
my $userAgent = "proxyScan/0.1";


######################################################################
# main()

&getArgs;

# process each target host separated by comma's.
foreach my $targetHost (split(/,/, $targets)) {
	# check if it's an IP range
	if ($targetHost 
		=~ /^(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)$/) {

		# save start and end of range as decimal
		my $startIp 	= &ip2dec($1);
		my $endIp	= &ip2dec($2);

		# sanity check the range
		if ($startIp > $endIp) {
			print "$0: startIp is greater than endIp ";
			print "in $targetHost\n";
			die;
		}

		# iterate each IP address in the range
		for (my $dec=$startIp; $dec <= $endIp; $dec++) {

			# scan each IP by for each port
			foreach my $targetPort (split(/,/, $ports)) {

				# if the port is a range
				if ($targetPort =~ /^(\d+)-(\d+)$/) {
					my $startPort = $1;
					my $endPort   = $2;

					if ($startPort > $endPort) {
						print "$0: startPort is",
						 " greater than endPort",
						 " in $targetPort\n";
						die;
					}

					for (my $port=$startPort; 
					     $port <= $endPort; $port++) {
						my $ip=&dec2ip($dec);
						&scanPort($ip,$port);
					}

				# otherwise a single port
				} else {
					my $ip=&dec2ip($dec);
					&scanPort($ip,$targetPort);
				}
			}
		}

	# process single IP's, or hostnames
	} else {

		# scan this host for each port
		foreach my $targetPort (split(/,/, $ports)) {

			# if the port is a range
			if ($targetPort =~ /^(\d+)-(\d+)$/) {
				my $startPort = $1;
				my $endPort   = $2;

				if ($startPort > $endPort) {
					print "$0: startPort is",
					 " greater than endPort",
					 " in $targetPort\n";
					die;
				}

				for (my $port=$startPort; 
				     $port <= $endPort; $port++) {
					my $ip=$targetHost;
					&scanPort($ip,$port);
				}

			# otherwise a single port
			} else {
				my $ip=$targetHost;
				&scanPort($ip,$targetPort);
			}
		}

	}
}

# the end, only funtions from here on 
exit;


######################################################################
# Check and set options from command line args
#
sub getArgs() {
	Getopt::Long::Configure('bundling', 
        	'no_ignore_case');

	my $optVerbose;
	my $optHelp;
	my $optPorts;
	my $optTimeout;
	my $optDelay;
	my $optMethod;
	my $optTargets;

	GetOptions
		("v|verbose"    => \$optVerbose,
		"h|help"        => \$optHelp,
		"p|ports=s"     => \$optPorts,
		"o|timout=s"    => \$optTimeout,
		"d|delay=s"     => \$optDelay,
		"m|method=s"    => \$optMethod,
		"t|targets=s"   => \$optTargets);

	if ($optHelp) { # then help / usage option
		print "Usage: $0 [options below]\n";
		print "Options:\n";
		print "   --help",
		"\tthis message.\n";
		print "   --verbose",
		"\tbe verbose for debugging.\n";
		print "   --ports",
		"\tports to scan for.\n";
		print "\t\tExample: 80-90,8080-8090,443,23,22\n";
		print "   --targets",
		"\ttarget hosts to scan for through proxy. Default is localhost.\n";
		print "\t\tExample: localhost,10.1.1.1-10.1.1.100,myhost.somedomain.com\n";
		print "   --timeout",
		"\ttimeout in seconds to wait for a response. default is 2 seconds\n";
		print "   --delay",
		"\tdelay in seconds between requests. Default is 0.5.\n";
		print "   --method",
		"\trequest method (CONNECT/GET/OPTIONS/TRACE/etc). default is GET.\n";
		print "\n";
		print "Set proxy with environment variables *_proxy.  ";
		print "Example: export http_proxy=http://proxy.my.place:8080/\n\n";
		exit;
	}


	if ($optVerbose) {         # set debugging / verbose output
        	$DEBUG=1;
	} else {
		# default
        	my $DEBUG=0;
	}

	if ($optPorts) {         # ports to scan through
		if ($optPorts =~ /^[\d,-]+$/) {
			$ports = $optPorts;
		} else {
			die "$0: invalid ports.\n";
		}
	} else {
		# default port to 80
		$ports = "80";
	}

	if ($optTargets) {         # target hosts to scan through proxy
		if ($optTargets =~ /^[\d\w\.,-]+$/) {
			$targets = $optTargets;
		} else {
			die "$0: invalid targets.\n";
		}
	} else {
		# default targets to localhost only
		$targets = "localhost";
	}

	if ($optTimeout) {         # timout in secs for a response
		if ($optTimeout =~ /^\d+$/) {
			$timeout = $optTimeout;
		} else {
			die "$0: invalid timeout.\n";
		}
	} else {
		# default timeout
		$timeout = "2";
	}

	if ($optDelay) {         # delay in secs between request
		if ($optDelay =~ /^\d+$/) {
			$delay = $optDelay;
		} else {
			die "$0: invalid delay.\n";
		}
	} else {
		# default delay
		$delay = "0.5";
	}

	if ($optMethod) {         # HTTP method
		if ($optMethod =~ /^\w+$/) {
			$method = uc($optMethod);
		} else {
			die "$0: invalid method.\n";
		}
	} else {
		# default method
		$method = "GET";
	}
}

######################################################################
# Scan for a target and port 
#
sub scanPort() {

	my $target = shift 
		|| die "$0: no target passed to scanPort()\n";

	my $port = shift 
		|| die "$0: no port passed to scanPort()\n";

	if ($target && $port) {

		# Create a user agent object
		my $ua = LWP::UserAgent->new;
		$ua->agent("$userAgent ");
		$ua->timeout($timeout);
		$ua->env_proxy;
		my $url = "http://".$target.":".$port;

		if ($DEBUG) {
			if ($ENV{http_proxy}) {
				print "proxy = $ENV{http_proxy}\n";
			} else {
				print "proxy = [NOT SET]\n";
			}
			print "port = $port\n";
			print "target = $target\n";
			print "url = $url\n";
		}

		# Create a request
		my $req = HTTP::Request->new($method => $url);

		# Pass request to the user agent and get a response back
		my $res = $ua->request($req);

		# Check the outcome of the response
		my $passFail;;
		if ($res->is_success) {
			$passFail="pass";	
		} else {
			$passFail="fail";	
		}

		print "result=\"$passFail\",";
		print "URL=\"$url\",";
		print "method=\"$method\",";

		if ($ENV{http_proxy}) {
			print "proxy=\"$ENV{http_proxy}\",";
		} else {
			print "proxy=\"[NOT SET]\",";
		}

		print "result=\"".$res->status_line, "\"\n";
		# uncomment for the response content
		#print $res->content;


		# sleep a while based on the delay set
		# the delay is important.  without this LWP
		# will send out request as fast as it can and
		# we may miss the response.
		sleep($delay);

	} else {
		die "$0: you must specify at least on host and one port\n";
	}
}

######################################################################
# Convert IP addresses to decimal for use with ranges
#
sub ip2dec() {
	my $hex;
	my $ip = shift || return;

	# Sanity check arguments and example regex of an IP address, almost.
	if ($ip !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/ ) {
  		die "$0: Invalid IP address given to ip2dec - $ip\n";
	}

	# Convert to Hex
	foreach my $octet (split(/\./,$ip, 4)) {
  		die "Invalid IP address given\n" 
			if($octet < 0 || $octet > 255);
  		$hex .= sprintf("%02x",$octet);
	}

	# Convert to decimal and return
	return hex($hex);
}

######################################################################
# Convert Decimal to IP address
#
sub dec2ip {
	my $dec = shift || return;

	# Sanity check arguments 
	if ($dec !~ /^\d+$/ ) {
  		die "$0: Invalid decimal IP given to dec2ip - $dec\n";
	}
        my $hexagain = sprintf("%08x", $dec);
        my $octet1 = substr($hexagain,0,2);
        my $octet2 = substr($hexagain,2,2);
        my $octet3 = substr($hexagain,4,2);
        my $octet4 = substr($hexagain,6,2);
        my $dec1 = hex($octet1);
        my $dec2 = hex($octet2);
        my $dec3 = hex($octet3);
        my $dec4 = hex($octet4);
        return "$dec1.$dec2.$dec3.$dec4";
}
