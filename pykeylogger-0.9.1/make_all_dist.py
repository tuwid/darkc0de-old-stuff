import version
import os
import sys

import zipfile
import zlib


def ZipFiles(targetdir, ziparchivename):
    '''Create a zip archive of all files in the target directory.
    '''
    #os.chdir(targetdir)
    myzip = zipfile.ZipFile(ziparchivename, "w", zipfile.ZIP_DEFLATED)
    
    if type(targetdir) == str:
        for root, dirs, files in os.walk(targetdir):
            for fname in files:
                if fname != ziparchivename:
                    myzip.write(os.path.join(root,fname))
    if type(targetdir) == list:
        for fname in targetdir:
            myzip.write(fname)
    
    myzip.close()
    myzip = zipfile.ZipFile(ziparchivename, "r", zipfile.ZIP_DEFLATED)
    if myzip.testzip() != None:
        print "Warning: Zipfile did not pass check."
    myzip.close()

if __name__ == '__main__':

    if raw_input("Current version is " + version.version + ". Is that correct? [Y/N] ") in ["y", "Y", "yes", "YES", "Yes"]:
        pass
    else:
        sys.exit()
        
    fname_addendum = raw_input("Filename addendum (start with '_')? ")

    #delete old build dir.
    print r'rd /S /Q build'
    os.system(r'rd /S /Q build')
    
    #delete old dist dir
    print r'rd /S /Q dist'
    os.system(r'rd /S /Q dist')

    # create the exe 
    print r'c:\Python25\python setup.py py2exe'
    os.system(r'c:\Python25\python setup.py py2exe')

    #pause to see output
    #os.system('pause "done, press key to continue"')
    print r'rename "dist" "pykeylogger-' + version.version + '""'
    os.system(r'rename "dist" "pykeylogger-' + version.version + '""')

    #~ print r'copy ".\*.txt" ".\pykeylogger""'
    #~ os.system(r'copy ".\*.txt" ".\pykeylogger""')

    #~ print r'copy ".\pykeylogger.ini" ".\pykeylogger""'
    #~ os.system(r'copy ".\pykeylogger.ini" ".\pykeylogger""')

    #command = '\"\"C:\Progra~1\WinRAR\WinRAR.exe" a -r "pykeylogger' + version.version + '_win32.zip" "pykeylogger\"\"'
    #print repr(command)
    #os.system(command)
    print "zipping executables"
    ZipFiles(r"pykeylogger-" + version.version, "pykeylogger-" + version.version + fname_addendum + "_win32.zip")
    
    #print r'""C:\Progra~1\WinRAR\WinRAR.exe" a -r "pykeylogger' + version.version + '_win32.zip" "pykeylogger""'
    #os.system(r'""C:\Progra~1\WinRAR\WinRAR.exe" a -r "pykeylogger' + version.version + '_win32.zip" "pykeylogger""')

    print r'rd /S /Q pykeylogger-' + version.version
    os.system(r'rd /S /Q pykeylogger-' + version.version)
    print r'rd /S /Q build'
    os.system(r'rd /S /Q build')

    os.system(r'pause "done, now lets create the src dist"')
    #sys.exit()
    #print r'""C:\Progra~1\WinRAR\WinRAR.exe" a -r "pykeylogger' + version.version + '_src.zip" "keylogger.pyw" "logwriter.py" "setup.py" "mytimer.py" "version.py" "make_all_dist.py" "*.txt" "*.bat" "html""'
    #os.system(r'""C:\Progra~1\WinRAR\WinRAR.exe" a -r "pykeylogger' + version.version + '_src.zip" "keylogger.pyw" "logwriter.py" "setup.py" "mytimer.py" "version.py" "make_all_dist.py" "*.txt" "run_exe_pykeylogger_with_cmdoptions.bat" "run_pykeylogger_with_cmdoptions.bat" "html""')

    #print "zipping sources"
    #ZipFiles(["keylogger.pyw","logwriter.py","setup.py","mytimer.py","version.py","make_all_dist.py","pykeylogger.ini","LICENSE.txt","CHANGELOG.TXT","TODO.txt","README.txt"], "pykeylogger" + version.version + "_src.zip")
    print "creating sdist"
    os.system(r'c:\Python25\python setup.py sdist')

    print r'move ".\dist\pykeylogger-' + version.version + r'.zip" ".\pykeylogger-' + version.version + fname_addendum + '_src.zip"'
    os.system(r'move ".\dist\pykeylogger-' + version.version + r'.zip" ".\pykeylogger-' + version.version + fname_addendum + '_src.zip"')

    print r'rd /S /Q dist'
    os.system(r'rd /S /Q dist')

    #os.system('pause "now lets create the md5 sums"')
    print r'""C:\Progra~1\UnixUtils\md5sum.exe" "pykeylogger-' + version.version + fname_addendum + r'_src.zip" > "..\pykeylogger-' + version.version + fname_addendum + '_src_md5sum.txt""'
    os.system(r'""C:\Progra~1\UnixUtils\md5sum.exe" "pykeylogger-' + version.version + fname_addendum + r'_src.zip" > "..\pykeylogger-' + version.version + fname_addendum + '_src_md5sum.txt""')
    print r'""C:\Progra~1\UnixUtils\md5sum.exe" "pykeylogger-' + version.version + fname_addendum + r'_win32.zip" > "..\pykeylogger-' + version.version + fname_addendum + '_win32_md5sum.txt""'
    os.system(r'""C:\Progra~1\UnixUtils\md5sum.exe" "pykeylogger-' + version.version + fname_addendum + r'_win32.zip" > "..\pykeylogger-' + version.version + fname_addendum + '_win32_md5sum.txt""')

    print r'move ".\pykeylogger-' + version.version + fname_addendum + r'_win32.zip" "..\pykeylogger-' + version.version + fname_addendum + '_win32.zip"'
    os.system(r'move ".\pykeylogger-' + version.version + fname_addendum + r'_win32.zip" "..\pykeylogger-' + version.version + fname_addendum + '_win32.zip"')

    print r'move ".\pykeylogger-' + version.version + fname_addendum + r'_src.zip" "..\pykeylogger-' + version.version + fname_addendum + '_src.zip"'
    os.system(r'move ".\pykeylogger-' + version.version + fname_addendum + r'_src.zip" "..\pykeylogger-' + version.version + fname_addendum + '_src.zip"')


    os.system(r'pause "done, press to key to exit""')
