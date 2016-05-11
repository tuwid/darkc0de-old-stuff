#!/usr/bin/python 
# dpc-hashcrack.py v1.0 
# offline cracking tools for md5,sha1,sha224,sha256,sha384,sha512 using 
# Crochemore-Perrin algorithm /w multiprocessing module. List dictionary will 
# be divided of 2 parts. reading string list from top to bottom and bottom 
# to top until the middle position of the number of strings, to increase 
# the probability and effectiveness discover of the password 
# 
# c0der: ch3cksum   <ch3cksum@depredac0de.net> 
# special thx to: 5ynL0rd,xco,Dr_EIP,gat3w4y,pyfla,acayz,B4dJoe,blackend, 
#                 g4pt3k,qrembiezs,boys_rvn1609,Unixc0de 
# special thx community: darkc0de & antijasakom 
# 
# depredac0de.net <underground network security research group> 
#****************************************************************************************** 
import multiprocessing,hashlib,sys,os 
 
def md5(hash): 
	climax = hashlib.md5(hash).hexdigest() 
	return climax 
def sha1(hash): 
	climax = hashlib.sha1(hash).hexdigest() 
	return climax 
def sha224(hash): 
        climax = hashlib.sha224(hash).hexdigest() 
        return climax 
def sha256(hash): 
        climax = hashlib.sha256(hash).hexdigest() 
        return climax 
def sha384(hash): 
        climax = hashlib.sha384(hash).hexdigest() 
        return climax 
def sha512(hash): 
        climax = hashlib.sha512(hash).hexdigest() 
        return climax 
 
def getbigdick(penis): 
	try: 
		pussy = open(penis,'r') 
		licker = pussy.readlines() 
		c1 = 0 
		while c1 < len(licker): 
			licker[c1] = licker[c1].strip() 
			c1 += 1 
	except IOError: 
		print "[-] Your file cannot be suck!" %penis 
		exit() 
	else: 
		cek = len(licker) 
		print "[+] %s word loaded" %cek 
		return licker 
 
def toptobottom(crack): 
	i = 0 
	while i < (len(asshole)/2): 
		if len(crack) == 32: 
			if crack == md5(asshole[i]): 
				print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
				break 
		elif len(crack) == 40: 
			if crack == sha1(asshole[i]): 
				print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
				break 
                elif len(crack) == 56: 
                        if crack == sha224(asshole[i]): 
                                print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
                                break 
                elif len(crack) == 64: 
                        if crack == sha256(asshole[i]): 
                                print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
                                break 
                elif len(crack) == 96: 
                        if crack == sha384(asshole[i]): 
                                print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
                                break 
                elif len(crack) == 128: 
                        if crack == sha512(asshole[i]): 
                                print "\n\t[p1] 3===D  passwd is = %s\n"%asshole[i] 
                                break 
                else: 
			print "[-] not support hash" 
			sys.exit() 
		i += 1 
def bottomtotop(crack): 
	k = 0 
	big = len(asshole) - len(asshole)/2 
	while k < (big): 
		if len(crack) == 32: 
			if crack == md5(asshole[-k]): 
				print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
				break 
		elif len(crack) == 40: 
                        if crack == sha1(asshole[-k]): 
                                print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
                                break 
                elif len(crack) == 56: 
                        if crack == sha224(asshole[-k]): 
                                print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
                                break 
                elif len(crack) == 64: 
                        if crack == sha256(asshole[-k]): 
                                print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
                                break 
                elif len(crack) == 96: 
                        if crack == sha384(asshole[-k]): 
                                print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
                                break 
                elif len(crack) == 128: 
                        if crack == sha512(asshole[-k]): 
                                print "\n\t[p2] 3===D  passwd is = %s\n"%asshole[-k] 
                                break 
		else: 
			sys.exit() 
		k += 1 
 
def banner(): 
	header = ''' 
_______________________________________________________________________ 
 dpc-hashcrack.py v1.0 
                     "Take di*k out 3===D x" 
                                .-. 
                               (/^\) 
                               (\ /) 
                               .-'-. 
                              /(_I_)\ 
                              \\\\) (// 
                               / v \ 
                               \ | / 
                                \|/ 
                                /|\ 
                                \|/ 
                                /Y\\ 
 
c0der: ch3cksum   <ch3cksum@depredac0de.net> 
special thx to: 5ynL0rd,xco,Dr_EIP,gat3w4y,pyfla,acayz,B4dJoe,blackend, 
                g4pt3k,qrembiezs,boys_rvn1609,Unixc0de 
________________________________________________________________________''' 
	print header 
 
if __name__=="__main__": 
	if os.name == "posix": 
		refresh = "clear" 
	else: 
		refresh = "cls" 
        os.system(refresh) 
	banner() 
	fuckit = raw_input("[+] Enter the Fuckin hash: ") 
	dick = raw_input("[+] Enter dick file: ") 
	asshole = getbigdick(dick) 
	p1 = multiprocessing.Process(target=toptobottom, args=[fuckit]) 
	p2 = multiprocessing.Process(target=bottomtotop, args=[fuckit]) 
	p1.start() 
	p2.start() 
	while 1: 
		if p1.is_alive()==False: 
			p2.terminate() 
			print "\n" 
			break 
		if p2.is_alive()==False: 
			p1.terminate() 
			print "\n" 
			break 