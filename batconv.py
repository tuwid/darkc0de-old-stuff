########################################################################
#
#   EXE to BAT converter Version 2.0                                   #
#   Much improved EXE2BAT script with base 64 decode COM stub and no   #
#   size limits.                                                       #
#                                                                      #
#                                        rattle | awarenetwork | org   #
                                                                       #
########################################################################

from base64 import encodestring
from sys import argv as a, exit, stdout
die = lambda x,n: stdout.write(x+'\n') or exit(n)

try:
 a[1] = a[1].upper()
 f,b = open(a[1]+'.exe','rb'),open(a[1]+'.bat','w')
except: 
 die('[!] usage: e2b.py <name>',1);

b.write('@ECHO OFF\nSET E=ECHO\nDEL D 1>NUL 2>NUL\n')

b.write(''.join(map(lambda x:'%%E%% %s>>D\n'%x, """
E 0100 31 C9 3E 8A 0E 80 00 89 CF 81 C7 81 00 3E C6 45
E 0110 00 00 4F 3E 80 7D 00 20 75 F8 3E C6 45 00 00 89
E 0120 FA 42 B4 3C B9 02 00 CD 21 72 7D 89 C7 B8 00 3D
E 0130 BA 82 00 CD 21 72 7D 89 C6 31 C0 89 C3 89 E2 81
E 0140 EA 04 00 B9 01 00 53 50 B4 3F 89 F3 CD 21 58 5B
E 0150 72 5C 3D 46 4F 75 06 81 FB 45 3A 74 08 88 DF 88
E 0160 E3 88 C4 EB E1 B8 01 42 89 F3 31 C9 BA 02 00 CD
E 0170 21 72 3B B9 13 00 51 81 EC 04 00 B4 3F 89 F3 B9
E 0180 04 00 89 E2 CD 21 72 26 85 C0 74 16 E9 3D 00 B4
E 0190 40 89 FB 89 E2 CD 21 72 15 81 C4 04 00 59 E2 D6
E 01A0 EB C3 B9 00 4C E9 12 00 B9 01 4C E9 1A 00 B9 01
E 01B0 4C E9 06 00 B9 01 4C E9 07 00 B8 3E 00 89 FB CD
E 01C0 21 B8 3E 00 89 F3 CD 21 89 C8 CD 21 5B 58 31 D2
E 01D0 89 D1 80 FB 60 7F 20 80 FB 40 7F 15 80 FB 2B 74
E 01E0 1C 80 FB 2F 74 1C 80 FB 3D 74 3A 80 C3 04 E9 16
E 01F0 00 80 EB 41 E9 10 00 80 EB 47 E9 0A 00 B3 3E E9
E 0200 05 00 B3 3F E9 00 00 51 C1 E2 06 C1 E9 02 08 EA
E 0210 08 CB 59 88 DD 88 FB 88 C7 88 E0 FE C1 80 F9 04
E 0220 75 B0 E9 24 00 81 F9 02 00 75 0A 88 D6 88 EA C1
E 0230 E2 04 E9 0B 00 C1 E2 06 C0 E1 02 C1 E9 02 08 CA
E 0240 86 D6 31 C0 50 52 E9 08 00 88 E8 30 E4 50 86 D6
E 0250 52 30 ED 49 E9 38 FF\nN B64.COM\nRCX\n157\nW\nQ
""".strip().split("\n"))))

b.write("""DEBUG<D 1>NUL\nB64.COM %s.BAT %s.EXE
IF ERRORLEVEL 1 THEN GOTO O\n%s.EXE\n:O
GOTO:EOF\n""" % (a[1],a[1],a[1]))

b.write(encodestring(f.read()));
