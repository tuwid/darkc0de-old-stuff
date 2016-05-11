# A very simple setup script to create an executable.
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them keylogger.exe and keylogger_debug.exe.


from distutils.core import setup
import py2exe
import version

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    name = version.name,
    version = version.version,
    description = version.description,
    url = version.url,
    license = version.license,
    author = version.author,
    author_email = version.author_email,
    platforms = [version.platform],

    data_files = [("",["pykeylogger.ini",
                        "pykeylogger.val",
                        "CHANGELOG.TXT",
                        "LICENSE.txt",
                        "README.txt",
                        "TODO.txt"])],
    # targets to build
    console = [
        {
            "script": "keylogger.pyw",
            "dest_base": "keylogger_debug"
        }
    ],
    
    windows = [
       {
           "script": "keylogger.pyw",
           "dest_base": "keylogger"
       }
    ],
    )

