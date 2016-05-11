#!/usr/bin/env python

VERSION = "\"0.4.4\""

import distutils

from distutils.core import Extension, setup

setup(name='Billy the Kid',
      version=VERSION,
      maintainer='Gorny',
      maintainer_email='gorny0@zonnet.nl',
      ext_modules=[Extension('btk',
             ['btk.c', 'btk_obj.c', 'packet.c', 'pcap.c'], libraries=["pcap"],
							define_macros=[('VERSION', VERSION)])
                   ],
      )
