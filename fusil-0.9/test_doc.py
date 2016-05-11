#!/usr/bin/python
from doctest import testfile, ELLIPSIS, testmod
from sys import exit, path as sys_path
from os.path import dirname

def testDoc(filename, name=None):
    print "--- %s: Run tests" % filename
    failure, nb_test = testfile(
        filename, optionflags=ELLIPSIS, name=name)
    if failure:
        exit(1)
    print "--- %s: End of tests" % filename

def importModule(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def testModule(name):
    print "--- Test module %s" % name
    module = importModule(name)
    failure, nb_test = testmod(module)
    if failure:
        exit(1)
    print "--- End of test"

def main():
    fusil_dir = dirname(__file__)
    sys_path.append(fusil_dir)

    # Test documentation in doc/*.rst files
    testDoc('doc/c_tools.rst')
    testDoc('doc/file_watch.rst')
    testDoc('doc/mangle.rst')

    # Unit tests as reST
    testDoc('tests/file_watch_read.rst')
    testDoc('tests/cmd_help_parser.rst')

    # Test documentation of some functions/classes
    testModule("fusil.tools")
    testModule("fusil.fuzzer.python")

if __name__ == "__main__":
    main()

