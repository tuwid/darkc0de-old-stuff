 
#!/usr/bin/env python 
import sys,os 
print """ ================================== 
|| (Eval encoded file) decrypter  || 
||       C0ded By AL-MoGrM        || 
||       WwW.darkc0de.CoM         || 
||   t0v [At] Hotmail [Dot] Com   || 
 ==================================""" 
if(len(sys.argv)<2): 
	print "|| Usage: ./%s <file>"%(sys.argv[0]); 
	print "|| ex: python %s file.php"%(sys.argv[0]); 
	print " ==================================" 
	sys.exit(1); 
if not os.path.isfile(sys.argv[1]): 
	print "|| [Error] Chack File Name ..."; 
	sys.exit(" ==================================") 
newname=os.path.basename(sys.argv[1])+".de" 
encode= file(sys.argv[1],'r').read()+";" 
 
x= encode.replace("<?php","").replace("<?","").replace('$','\$').replace("?>","").replace("eval","echo").replace("\$_F=.\$_F.;","\$_F=\$_F;") 
xs=os.system('php -r "%s">x.2'%(x)) 
x2=file("x.2",'r').read().replace("eval","echo"); 
if "$_X=base64_decode($_X);$_X=strtr(" in x2 : 
	x3=x[:x.find('echo')]+x2.replace("$","\$") 
	xs=os.system('php -r "%s">x.2'%(x3)) 
 
os.rename("x.2",newname); 
print "|| [DONE] Read file => %s"%newname 
print " ==================================" 

