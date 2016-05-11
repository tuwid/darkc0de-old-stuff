### setup.py ###
from distutils.core import setup

setup (name='STAR',
      version='1.0',
      description='RATS Graphical Frontend.',
      author='Benjamin Lull',
      author_email='benjaminlull@earthlink.net',
      url='http://www.socialnetworkwhore.com/',
      license='MIT',
      scripts=['star'],
      py_modules=['About', 'Alert', 'MainWindow', 'Settings'],
)
