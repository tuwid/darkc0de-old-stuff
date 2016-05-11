from distutils.core import setup, Extension

module1 = Extension('ulibzeppoo',
                    sources = ['ulibzeppoo.c'])

setup (name = 'PackageName',
       version = '0.0.1',
       description = 'Ulib Zeppoo',
       ext_modules = [module1])
