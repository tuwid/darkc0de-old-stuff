#! /usr/bin/env python
# REQUIREMENTS:
# libnids (and libnet 1.0.2a, libpcap)
# python 2.2 or later
# pynids: http://pilcrow.madison.wi.us/pynids/
#
#  Copyright (C) 2006  Sebastian Garcia
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Author:
# sgarcia@citefa.gov.ar
#
# Changelog
# 0.6
# 	Added support for special Ssh client version provided by the user
# 	Added default medusa ssh password cracker SSH string. Medusa doest'n use 'libssh' as hydra, it uses 'MEDUSA'
# 	Added printing of destination Ip address and destination port (usually the ssh server port). This is handy when you have multiple honeypots and when your honeypot is starting an ssh connection (This was a TODO until Carlos Benitez need it. Thanks)
# 	As libnids doesn't give us any packet capture time, we can't filter based in the amount of connections per minute!!!
#	Deleted some unused variables
#	Deleted default destination port filtering, we solely rely on the SSH- string passing by
#	SSH version string get better, we now look after the SSH- string both in the server stream and in the client stream. This wast'n implemented in sshow
# 	Added support for byte count filtering of interactive sessions.
#	Added real support for -t flag, allowing the user to change the type of interactive seession filtering.
#	Added the -b flag, allowing the user to change the mininum amount of bytes an interactive session must have.
#
# 0.5 0.4-alpha Released as 0.5
#
# 0.4-alpha : 29-11-2006/1-12-2006
# 	We migrate everything to the new data structure. See details below
#	Incorporation of new Interactive filtering through a centralizes function
#	A lot of comment changes
#
# 0.4: 3-11-2006
# 	Fixed the never ending connections bug. Where we lost connections that did't end before we stop capture.
#	At the end states, we trust in the global filter and do not re-filter destination ports
#	Fixed the output help when you don't use any options
#	Now every exception handling code prints out in which funcion it has been called
#	
#
# 0.3: 2-11-2006
#	Fixed some bugs with dev capturing (thanks to leandro ferrari - talsoft@flash.com.ar)
#	Added support for online reporting, because we never stop processing the packets
#	
# 0.2: 1-11-2006
#	Added our ssh ports
#	Added support for getopt, help, and pcap file captures
#
# 0.1 30-10-2006
#	Is a copy of versiondetect.py from pynids package
#
# TODO
# - If the input file is too big, perhaps it's better to pause processig new packets after some time/length, output results and continue processing packets.
# - There are problemas with the session counter, we think it's not working properly. One of fede's tcpdumps show this.????????????
#
# KNOWN BUGS
# - We can't process tcpdump files larger than 100Mb, i don't know why. The sniffer hangs.
#
# LIBNIDS - PCAP problem
# - Libnids it's very slow processing big files. A file of 2Gb it's not rare in our enviroment and ssh-version0.5 takes 100 minutes to process it. What can we do to get this better?
#
# Internal Structure:
# 
# response_dict  (main dictionary. The client ip address is it's key, and each Ip points to another dictionary)
#  |- 192.168.1.1 -> temp_header_dict (it's keys are the SSH versions uses by THIS IP. Points to another dict)
#  |- 192.168.1.2 -> temp_header_dict (it's keys are the SSH versions uses by THIS IP. Points to another dict)
#                     |- SSH-Ver1 -> cli_sport_dict (it's key is the source port)
#                     |- SSH-Ver2 ->  |- 1024 -> uniq_id_dict (Incremental ID for this IP-SSHVERSION-SRCPORT. it's key is an integer)
#                                     |- 1026     |- 2 -> [140.4.17.12, sshd-version, 22, 3300] (dst Ip, dst ssh ver, dst port, amount of bytes transfer in both directions)
#                                                 |- 3 -> [38.54.3.9, sshd-version, 222, 1070] (dst Ip, dst ssh ver, dst port, amount of bytes transfer in both directions)

#
# Under python terminology, you will see this for example: {'192.168.1.1': {'SSHVer': {1024: {1: ('192.168.1.2','SSHD-Ver',145, 1200)}}}}
#


# standard imports
import os, pwd, string, sys
import getopt

# local imports ...
import nids


####################
# Global Variables

# Default filter type to use when looking for interactive sessions
filter_by=''

# Min limit of bytes a connection must have to be interactive. Set by experience with real intruders
# WAS thit value until I found some extrange connection: cant_bytes_min = 2900
cant_bytes_min = 4000

# We never execute this program like root
NOTROOT = "nobody"   	# edit to taste

# States where tcp connections can end
end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)

# Default pcap capture filter
# Common ssh ports seen in the wild
#filter="port 26129 or port 45466 or port 34907 or port 22 or port 5555 or port 43434 or port 2022 or port 2222"
filter=""

# Debug
debug=0


# Where we store the response
response_dict={}

# Where we store the responses while in DATA state!
response_dict_data={}

#device
dev=""

# Sign, to print the sign just once.
sign=0

# Control if we print just the SSH2 interactive sessions
interactive=False

# Ssh client versin string to filter out given by the user
ssh_user_string = ""

# End of global variables
###########################








# Print version information and exit
def version():
  print "+--------------------------------------------------------------+"
  print "| Si6 Information Security Research Group - Citefa - Argentina |"
  print "| ssh-sniffer Version 0.6                                     |"
  print "+--------------------------------------------------------------+"
  print
  sys.exit(1)


# Print help information and exit:
def usage():
  print "+--------------------------------------------------------------+"
  print "| Si6 Information Security Research Group - Citefa - Argentina |"
  print "+--------------------------------------------------------------+"
  print "\nusage: %s <options>" % sys.argv[0]
  print "options:"
  print "  -i, --input-file    	Pcap file to open."
  print "  -d, --capture-device	While capturing from the net, use this device."
  print "  -h, --help         	Show this help message and exit"
  print "  -V, --version      	Output version information and exit"
  print "  -f, --filter      	Tcpdump pcap filter to apply. Default = \"udp and host 10.200.200.200\". Must be \"\" delimited."
  print "  -D, --debug    	Debug."
  #print "  -I, --interactive	Filter out and just print the interactive ssh sessions. Default filter is SSH client version."
  print "  -t, --session-type	Filter out and print interactive ssh sessions. Filter by (default all):\n\t\t\tversion: If SSH2 client version is 'libssh' or 'MEDUSA'\n\t\t\tbytes: If the amount of bytes on a connection is less than a value (2900 by default)\n\t\t\tall: Must acomplish all of them at the same time"
  print "  -b, --min-bytes	The minimal amount of bytes a connection must have to be considered interactive. (Default " + str(cant_bytes_min) + " bytes)"
  print "  -s, --ssh-string	Ssh client version string to filter besides 'libssh' and 'MEDUSA'. Without quotes."
  print
  sys.exit(1)




def handleTcpStream(tcp):
	try:
		import string
		global response_dict
		global debug
		global dev
		global sign

		if tcp.nids_state == nids.NIDS_JUST_EST:
			tcp.client.collect = 1
			tcp.server.collect = 1

		elif tcp.nids_state == nids.NIDS_DATA:
			# keep all of the stream's new data
			# Or do not discard any byte! bytes=0
			tcp.discard(0)

			# From now on this is the never ending connections fix
			clientheaders_data = string.split(tcp.server.data, "\n")	# grab client data
			serverheaders_data = string.split(tcp.client.data, "\n")	# grab server data
			clientheader=clientheaders_data[0]
			serverheader=serverheaders_data[0]
			
			client_ip_addr = tcp.addr[0][0]
			client_source_port = tcp.addr[0][1]
			server_ip_addr = tcp.addr[1][0]
			server_destination_port = tcp.addr[1][1]
			
			if serverheader.find('SSH-') == 0 and clientheader.find('SSH-') == 0:

				# For some reason sometimes we find that a carriage return was appended to the 
				# end, we chop it.
				if clientheader[len(clientheader)-1]=='\r':
					clientheader=clientheader[:-1]

				# Remember this are connections that NEVER END
				if not(response_dict_data.has_key(client_ip_addr)):
					# New IP 
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					next_id = 1
					# New IP so id is 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader,server_destination_port,cant_bytes]
					temp_sport_dict={}
					temp_sport_dict[client_source_port]=temp_uniq_id_dict
					temp_header_dict={}
					temp_header_dict[clientheader]=temp_sport_dict
					response_dict_data[client_ip_addr]=temp_header_dict

				elif response_dict_data.has_key(client_ip_addr) and not(response_dict_data[client_ip_addr].has_key(clientheader)):
					# New ssh version for the same IP
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					# New IP so id is 1
					next_id = 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader,server_destination_port,cant_bytes]
					temp_sport_dict={}
					temp_sport_dict[client_source_port]=temp_uniq_id_dict

					# Recover previous header_dict	
					previous_temp_header_dict=response_dict_data[client_ip_addr]
					previous_temp_header_dict[clientheader]=temp_sport_dict

					response_dict_data[client_ip_addr]=previous_temp_header_dict

				elif response_dict_data.has_key(client_ip_addr) and response_dict_data[client_ip_addr].has_key(clientheader) and not(response_dict_data[client_ip_addr][clientheader].has_key(client_source_port)):
					# New source port for the same IP and SSh Version
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					# New IP so id is 1
					next_id = 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader,server_destination_port,cant_bytes]
					
					# Recover previous temp sport dict	
					previous_temp_sport_dict=response_dict_data[client_ip_addr][clientheader]
					previous_temp_sport_dict[client_source_port]=temp_uniq_id_dict

					response_dict_data[client_ip_addr][clientheader]=previous_temp_sport_dict

				elif response_dict_data.has_key(client_ip_addr) and response_dict_data[client_ip_addr].has_key(clientheader) and response_dict_data[client_ip_addr][clientheader].has_key(client_source_port):
					# Yes, we can have multiple not ended conection in this situation. We found the same Ip-Sshversion-srcport stored in our dictionary, we must do something!
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					next_id = 1

					# We don't know how to diferentiate between an already established-nonEnded connection and the
					# next established-nonEnded connection using the same Ip-SSHVer-SrcPort. This can be very
					# dificult
					previous_temp_uniq_id_dict={}
					previous_temp_uniq_id_dict[1]=[server_ip_addr,serverheader,server_destination_port,cant_bytes]

					response_dict_data[client_ip_addr][clientheader][client_source_port]=previous_temp_uniq_id_dict

					if debug and dev!="" and interactive and interactive_session_filter(client_ip_addr,clientheader,client_source_port,cant_bytess):
						# This is to show the warning just once. Pretty ugly.
						if not(sign):
							sign=1
							print 'Warning!, Debug and network capture mode at the same time, shows up duplicate Ip:port connnections, due to Never ending connections code.'
						print ' - %-20s\t -> %-20s %-38s (Bytes: %d, Id:%d) Data state' % (client_ip_addr+':'+str(client_source_port),clientheader,serverheader,cant_bytes,next_id)	
					elif debug and dev !="": 
						if not(sign):
							sign=1
							print 'Warning!, Debug and network capture mode at the same time, shows up duplicate Ip:port connnections, due to Never ending connections code.'
						print ' - %-20s\t -> %-20s %-38s (Bytes: %d, Id:%d) Data state' % (client_ip_addr+':'+str(client_source_port),clientheader,serverheader,cant_bytes,next_id)	

		elif tcp.nids_state in end_states:
			clientheaders = string.split(tcp.server.data, "\n")	# grab client data
			serverheaders = string.split(tcp.client.data, "\n")	# grab server data
			clientheader=clientheaders[0]
			serverheader=serverheaders[0]
			
			client_ip_addr = tcp.addr[0][0]
			client_source_port = tcp.addr[0][1]
			server_ip_addr = tcp.addr[1][0]
			server_destination_port = tcp.addr[1][1]

			if serverheader.find('SSH-') == 0 and clientheader.find('SSH-') == 0:
				# For some reason sometimes we find that a carriage return was appended to the 
				# end, we chop it.
				if clientheader[len(clientheader)-1]=='\r':
					clientheader=clientheader[:-1]
				
				# Remember this are ended connections
				if not(response_dict.has_key(client_ip_addr)):
					# New IP 
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					next_id = 1
					# New IP so id is 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader ,server_destination_port,cant_bytes]
					temp_sport_dict={}
					temp_sport_dict[client_source_port]=temp_uniq_id_dict
					temp_header_dict={}
					temp_header_dict[clientheader]=temp_sport_dict
					response_dict[client_ip_addr]=temp_header_dict
				elif response_dict.has_key(client_ip_addr) and not(response_dict[client_ip_addr].has_key(clientheader)):
					# New ssh version for the same IP
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					# New IP so id is 1
					next_id = 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader,server_destination_port,cant_bytes]
					temp_sport_dict={}
					temp_sport_dict[client_source_port]=temp_uniq_id_dict

					# Recover previous header_dict	
					previous_temp_header_dict=response_dict[client_ip_addr]
					previous_temp_header_dict[clientheader]=temp_sport_dict

					response_dict[client_ip_addr]=previous_temp_header_dict

				elif response_dict.has_key(client_ip_addr) and response_dict[client_ip_addr].has_key(clientheader) and not(response_dict[client_ip_addr][clientheader].has_key(client_source_port)):
					# New source port for the same IP and SSh Version
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					temp_uniq_id_dict={}
					# New IP so id is 1
					next_id = 1
					temp_uniq_id_dict[next_id] = [server_ip_addr,serverheader,server_destination_port,cant_bytes]
					
					# Recover previous temp sport dict	
					previous_temp_sport_dict=response_dict[client_ip_addr][clientheader]
					previous_temp_sport_dict[client_source_port]=temp_uniq_id_dict

					response_dict[client_ip_addr][clientheader]=previous_temp_sport_dict

				elif response_dict.has_key(client_ip_addr) and response_dict[client_ip_addr].has_key(clientheader) and response_dict[client_ip_addr][clientheader].has_key(client_source_port):
					# We found the same Ip-Sshversion-srcport!! stored in our dictionary, we must do something!!!
					cant_bytes = tcp.server.count+tcp.client.count
					# it's the first
					
					# Recover previous temp uniq id dict	
					previous_temp_uniq_id_dict=response_dict[client_ip_addr][clientheader][client_source_port]
					last_id = previous_temp_uniq_id_dict.keys()[len(previous_temp_uniq_id_dict)-1]
					next_id = last_id + 1
					previous_temp_uniq_id_dict[next_id]=[server_ip_addr,serverheader,server_destination_port,cant_bytes]

					response_dict[client_ip_addr][clientheader][client_source_port]=previous_temp_uniq_id_dict

				# If we are capturing on real time or debuging
				if dev!="" or debug:
					print '  -- %-22s %-30s -> %-20s %-38s (Bytes: %d, Id:%s)' % (client_ip_addr+':'+str(client_source_port),clientheader,(server_ip_addr+':'+str(server_destination_port)),serverheader,cant_bytes,next_id)	

					
	except Exception, e:
		print "misc. exception in handleTcpStream:", e
	except:
		print 'Error in handleTcpStream'


def output():
	try:
		global debug
		global response_dict
		global response_dict_data
		global dev
		global interactive

		# See .items function under dictionaries for more info
		sorted_response_vect=response_dict.items()
		sorted_response_vect.sort()

		if debug:
			print '  -- End processing\n'

		interactive_connections_count = 0
		total_connections_count = 0

		for i in sorted_response_vect:
			# i is every register from this vector
			client_ip_addr= i[0]
			ssh_version_dict = i[1]

			for j in ssh_version_dict.items():
				# Now for every item inside ssh version vect for that Ip...
				ssh_version = j[0]
				client_source_port_dict = j[1]

				for k in client_source_port_dict.items():
					client_src_port = k[0]
					uniq_id_dict = k[1]
					for l in uniq_id_dict.items():
						uniq_id = l[0]
						[server_ip_addr,ssh_version_server,server_dst_port,c_bytes] = l[1] 
		
						total_connections_count = total_connections_count + 1
						if interactive and interactive_session_filter(client_ip_addr,ssh_version,client_src_port,c_bytes):
							interactive_connections_count = interactive_connections_count + 1
							print '%-22s %-30s -> %-20s %-40s (Bytes: %d, Id:%s)' % (client_ip_addr+':'+str(client_src_port),ssh_version,(server_ip_addr+':'+str(server_dst_port)),ssh_version_server,c_bytes,uniq_id)	
						elif not(interactive):
							# Print all of the ssh connections, not just the interactives ones
							print '%-22s %-30s -> %-20s %-40s (Bytes: %d, Id:%s)' % (client_ip_addr+':'+str(client_src_port),ssh_version,(server_ip_addr+':'+str(server_dst_port)),ssh_version_server,c_bytes,uniq_id)	
							
		
		######################	
		# We handle the output for connections that never end.
		sorted_response_vect=response_dict_data.items()
		sorted_response_vect.sort()


		for i in sorted_response_vect:
			# i is every register from this vector
			client_ip_addr= i[0]
			if not(response_dict.has_key(client_ip_addr)):
				ssh_version_dict = i[1]

				for j in ssh_version_dict.items():
					# Now for every item inside ssh version vect for that Ip...
					ssh_version = j[0]
					client_source_port_dict = j[1]

					for k in client_source_port_dict.items():
						client_src_port = k[0]
						uniq_id_dict = k[1]
						for l in uniq_id_dict.items():
							uniq_id = l[0]
							[server_ip_addr,ssh_version_server,server_dst_port,c_bytes] = l[1] 

							if interactive and interactive_session_filter(client_ip_addr,ssh_version,client_src_port,c_bytes):
								print '%-22s %-30s -> %-20s %-40s (Bytes: %d, Id:%s)' % (client_ip_addr+':'+str(client_src_port),ssh_version,(server_ip_addr+':'+str(server_dst_port)),ssh_version_server,c_bytes,uniq_id)	
								
							elif not(interactive):
								# Print all of the ssh connections, not just the interactives ones
								print '%-22s %-30s -> %-20s %-40s (Bytes: %d, Id:%s)' % (client_ip_addr+':'+str(client_src_port),ssh_version,(server_ip_addr+':'+str(server_dst_port)),ssh_version_server,c_bytes,uniq_id)	
	
	
		if interactive:
			print '(%d total SSH conections, %d interactive)' % (total_connections_count,interactive_connections_count)
		else:
			print '(%d total SSH conections)' % (total_connections_count)
		
		
	except Exception, e:
		print "misc. exception in output:", e
	except:
		print 'Error in output function'





def interactive_session_filter(client_ip_addr,ssh_version,client_first_source_port,cant_bytes):
	try:
		global debug
		global response_dict
		global dev
		global interactive
		global filter_by
		global cant_bytes_min
		global ssh_user_string

		if interactive:
			if filter_by == 'version':
				if ssh_version.find('libssh') >= 0 or ssh_version.find('MEDUSA') >= 0 or (ssh_user_string != "" and ssh_version.find(ssh_user_string) >= 0):
					return 0
				else:
					return 1
			elif filter_by == 'bytes': 
				if cant_bytes > int(cant_bytes_min):
					return 1
				else:
					return 0
			elif filter_by == 'all':
				if ssh_version.find('libssh') >= 0 or ssh_version.find('MEDUSA') >= 0 or (ssh_user_string != "" and ssh_version.find(ssh_user_string) >= 0) or cant_bytes <= int(cant_bytes_min):
					return 0
				else:
					return 1
				
			else:
				print 'Error in filter type.'
				sys.exit(1)

	except Exception, e:
		print "misc. exception in interactive_session_filter function:", e
	except:
		print 'Error in interactive_session_filter function'





def main():
	try:
		ifile=""
		global dev
		global filter
		global debug
		global response_dict
		global interactive
		global filter_by
		global cant_bytes_min
		global ssh_user_string

		(uid, gid) = pwd.getpwnam(NOTROOT)[2:4]
		os.setgroups([gid,])
		os.setgid(gid)
		os.setuid(uid)
		if 0 in [os.getuid(), os.getgid()] + list(os.getgroups()):
			print "error - drop root, please!"
			sys.exit(1)


		opts, args = getopt.getopt(sys.argv[1:], "d:hVi:qf:Dt:b:s:", ["device=","help","version","input-file=","filter=","--debug","session-type=","min-bytes=","ssh-string="])
	except getopt.GetoptError: usage()

	for opt, arg in opts:
	    if opt in ("-h", "--help"): usage()
	    if opt in ("-V", "--version"): version()
	    if opt in ("-i", "--input-file"): ifile = arg
	    if opt in ("-d", "--capture-device"): dev = arg
	    if opt in ("-f", "--filter"): filter = arg
	    if opt in ("-D", "--debug"): debug=1
	    #if opt in ("-I", "--interactive"): interactive=True
	    if opt in ("-t", "--session-type"): filter_by = arg
	    if opt in ("-b", "--min-bytes"): cant_bytes_min = arg
	    if opt in ("-s", "--ssh-string"): ssh_user_string = arg
	try:

		if filter_by != "":
			interactive = True

		if ifile!="" and dev=="":
			if debug:
				print 'Input File : %s' % (ifile)
        		nids.param("filename", ifile)
		elif ifile=="" and dev!="":
			if debug:
				print 'Capturing from device : %s' % (dev)
		elif ifile=="" and dev=="":
			usage()
			sys.exit(1)

		if filter:
			if debug:
				print 'Filter: %s' % (filter)
			nids.param("pcap_filter",filter)

		nids.param("scan_num_hosts", 0)  # disable portscan detection

		nids.init()

	 	nids.register_tcp(handleTcpStream)

		try:
			if debug:
				print '  -- Start processing'
			nids.run()
			output()
		except nids.error, e:
			print "nids/pcap error:", e
			output()
		except Exception, e:
			print "misc. exception (runtime error from user callback?):", e
			output()
		except KeyboardInterrupt:
			output()
			sys.exit(1)


	except KeyboardInterrupt:
		# CTRL-C pretty handling.
		print "Keyboard Interruption!. Exiting."
		sys.exit(1)
	except nids.error, e:
		print "nids/pcap error:", e


if __name__ == '__main__':
    main()
