#!/usr/bin/python

"""
Oracle Database PL/SQL Fuzzing Tool

Copyright (c) 2005, 2006 Joxean Koret, joxeankoret [at] yahoo.es

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import sys
import cx_Oracle

global connection

funnydata = ("TEST", "SYS", "XMLREF", '" || XMLREF() || "', 'TEST" A A ', "'", '"', "A"*30, "A"*100, "A"*128,"A"*256,"A"*512,"A"*1024,
                        "A"*2048,"A"*3000,"A"*4000,"A"*5000,"A"*6000,"A"*7000,"A"*8000,"A"*10000,"A"*15000,"A"*20000,"A"*25000,
                        "A"*30000,"A"*32767, -1, -2, 0, 1, 2, 2147483647, -2147483647, 2147483648, -2147483648,
                        "ROWID", "PRIMARY KEY", "%s%s%s%s%s%s%s", "%x%x%x%x%x%x", "%d%d%d%d%d%d",
                        "GRANT DBA TO TEST", "GRANT DBA TO PUBLIC", "SELECT * FROM DBA_USERS",
                        "' OR '1'='1", "AA' or ""TEST"".""XMLREF"" ","V1", "TEST.V1", '"TEST"."V1"',
                        None)

def fuzzData(data, index):
    global connection

    for x in funnydata:
        try:
            if type(x) is int:
                print "Data is number",x
            else:
                print "Data is " + str(x)[0:30] + " of length " + str(len(str(x)))

            varList = []

            for var in range(index):
                varList.append(x)

            cur = connection.cursor()
            cur.execute(data, varList)
            
        except:
            error = str(sys.exc_info()[1])

            if error.upper().find("ORA-00933") > -1 or error.upper().find("ORA-01756:") > -1 or error.upper().find("ORA-00923:") > -1:
                print "*** POSSIBLE SQL INJECTION FOUND ***"
            elif error.upper().find("ORA-03113") > -1:
                if len(str(x)) > 50:
                    print "*** POSSIBLE BUFFER OVERFLOW ***"
                else:
                    print "*** INSTANCE CRASHED ***"

                print "Reconnecting ... "
                connect()
            elif error.upper().find("ORA-00600") > -1:
                print "*** INTERNAL ERROR ***"
            elif error.upper().find("PLS-00306:") > -1:
                print "Currently unfuzzable :("
                continue
            elif error.upper().find("ORA-03114") > -1:
                print "We are not connected :?"
                connect()

            print error

def connect():
    global connection

    link    = "test/test@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.1.10)(PORT=1521)))"
    link += "(CONNECT_DATA=(SERVICE_NAME=orcl)))"

    connection = cx_Oracle.connect(link)
    connection.rollback()
    connection.commit()

def isFunc(data, index, cursorData):
    global connection
    
    try:
        varList = []

        data = """BEGIN
       """+ data + """("""

        index = 0
        for x in cursorData:
            index += 1

            if index == 1:
                data += str(x[1]) + "=>:" + str(index)
            else:
                data += "," + str(x[1]) + "=>:" + str(index)
        
        data += """);
end;"""

        for var in range(index):
            varList.append(None)

        cur = connection.cursor()
        cur.execute(data, varList)
        
        return 0
    except:
        error = str(sys.exc_info()[1])
        if error.upper().find("PLS-00221")> -1:
            return 1
        else:
            return 0
    
def die(msg):
    print msg
    sys.exit(0)

def main():
    global connection

    fuzzPackages = """
 select distinct owner           "Owner",
       package_name    "Package",       
       package_name    "Package",       
       package_name    "Package",       
       object_name     "Program_Unit"
  from sys.all_arguments x
 where argument_name is not null
   and not exists (select 1 from sys.all_arguments y
                    where x.owner = y.owner
                      and x.package_name = y.owner
                      and x.object_name = y.object_name
                      and x.data_level = y.data_level
                      and y.data_type not in ('VARCHAR2', 'RAW', 'NCHAR', 'BINARY_INTEGER', 'BINARY_FLOAT',
                    'CHAR', 'NVARCHAR2', 'NUMBER', 'FLOAT', 'LONG RAW')
                      and rownum = 1)
  order by owner, package_name, object_name
        """

    packageProcedures = """
select position        "Position",
       argument_name   "Argument",
       data_type       "Data type",
       initcap(in_out) "In_Out",
       owner            sdev_link_owner,
       package_name     sdev_link_name,
       'PACKAGE'        sdev_link_type
  from sys.all_arguments
 where argument_name is not null
   and owner = :1
   and (:2 is null or 
        instr(upper(object_name),upper(:3)) > 0 or
        instr(upper(package_name),upper(:4)) > 0 )
   and object_name = :5
   and data_type in ('VARCHAR2', 'RAW', 'NCHAR', 'BINARY_INTEGER', 'BINARY_FLOAT',
                    'CHAR', 'NVARCHAR2', 'NUMBER', 'FLOAT', 'LONG RAW')
  order by owner, package_name, object_name, position
        """

    connect()

    bStart = False

    try:
        cursor = connection.cursor()
        cursor.execute(fuzzPackages)
        result = """
        BEGIN
        """

        pkgName = ""
        
        func = 0

        print "Running first query. It may take a long while ... "
        totalProcs = 0

        for pkgData in cursor.fetchall():
            totalProcs += 1

            if not pkgData[1] is None:
                pkgName = pkgData[0] + "." + pkgData[1] + "." + pkgData[4]
            else:
                pkgName = pkgData[0] + "." + pkgData[4]

            procCursor = connection.cursor()
            procCursor.execute(packageProcedures, pkgData)

            procCursorData = procCursor.fetchall()

            func = isFunc(pkgName, len(procCursorData), procCursorData)

            if int(func) == 0:
                data = """BEGIN
                """ + pkgName + """("""
            else:
                data = """SELECT """ + pkgName + """("""

            index = 0
            prevX = None

            for x in procCursorData:
                if x == prevX:
                    continue

                prevX = x
                index += 1

                if index == 1:
                    if func == 0:
                        data += str(x[1]) + "=>:" + str(index)
                    else:
                        data += ":" + str(index)
                else:
                    if func == 0:
                        data += "," + str(x[1]) + "=>:" + str(index)
                    else:
                        data += ", :" + str(index)
            
            if func == 0:
                data += """);
end;"""
            else:
                data += """) from dual """

            print "----------"
            print data
            print "----------"

            fuzzData(data, index)

        connection.close()
    except Exception, e:
        print "Error",e
        print "While fuzzing index",totalProcs,"relative to",pkgName
        raise e
    
    print 
    print "Fuzzed",totalProcs,"procedure(s) and function(s)."
    print "Done."

if __name__ == "__main__":
    main()
