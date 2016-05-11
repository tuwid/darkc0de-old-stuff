###############################################################################
## tasks.py  -- see http://www.zeppoo.net                                    ##
##									     ##	
## The project zeppoo is (C) 2006 : contact@zeppoo.net			     ##
## This program is free software;            				     ##
## you can redistribute it and/or modify it under the terms of the GNU       ##
## General Public License as published by the Free Software Foundation;      ##
## Version 2. This guarantees your right to use, modify, and                 ##
## redistribute this software under certain conditions.                      ##
##      								     ##
## Source is provided to this software because we believe users have a       ##
## right to know exactly what a program is going to do before they run       ##
## it.                                                                       ##
##									     ##
## This program is distributed in the hope that it will be                   ##
## useful, but WITHOUT ANY WARRANTY; without even the implied                ##
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR                   ##
## PURPOSE. See the GNU General Public License for more details (            ##
## http://www.gnu.org/copyleft/gpl.html ).                                   ##
##                                                                           ##
###############################################################################

import string
import os

from struct import pack
from struct import unpack
from memory import Memory
from symbols import Symbols

class Tasks:
	def __init__(self) :
		self.map_tasks = {}
		self.list_tasks = []
	
class GVTasks:
	offset_list = 0
	offset_list_next = 0
	offset_name = 0
	offset_pid = 0
	offset_uid = 0

	# 4 differents ways to get tasks
	tasks_mem = Tasks()
	tasks_ps = Tasks()
	tasks_proc = Tasks()
	tasks_procforce = Tasks()
	tasks_kill = Tasks()

	tasks_check = Tasks()
	
	def __init__(self, mmemory, typeaccess=0) :
		if not isinstance(mmemory, Memory):
			raise TypeError("ERREUR")

		self.mmemory = mmemory
		self.symbols = Symbols(self.mmemory)
		self.typeaccess = typeaccess

	def getOffsetPid(self, data) :
		""" Find the offset of pid in the task_struct struct """
		i = 0
		find1 = find2 = -1
		offset = 0
		
		while((i < len(data)) and (offset == 0)) :
			if(find1 == 1):
				find2 = find1

			find1 = unpack("<L", data[i:i+4])[0]
			if(find1 == find2) :
				offset = i
			i = i + 4

		offset = offset + self.offset_list
		return offset

	def getOffsetUid(self, data) :
		""" Find the offset of uid in the task_struct struct """
 
		offset = data.find("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
		offset2 = data.rfind("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
		
		if(offset2 < 400) :
			offset = offset2 - 4
		
		offset = offset + self.offset_pid 
		return offset

	def getOffsetListNext(self, data) :
		""" Find the offset of next task in the list_head struct """
		
		i = 0
		first_addr = second_addr = find1 = find2 = 0
		offset = -1
		
		while((i < len(data)) and (offset == -1)) :
			second_addr = first_addr
			first_addr = unpack("<L", data[i:i+4])[0]
#			print first_addr
			if(first_addr == second_addr and first_addr > 0xc0000000 and i > 0x20):
				find2 = find1
				find1 = i
				if((find1-find2) == 16):
					offset = find2+20
			
			i = i + 4

		return offset
	
		
	def getOffsetList(self, data) :
		""" Find the offset of tasks in the task_struct struct """
		
		i = 0
		l = []
		count = 0
		prec = ""
		find = -1
		offset = 0

		for i in range(0, len(data), 4):
			var = "%x" % unpack("<L", data[i:i+4])[0]
			l.append(var)

		for j in l :
		#	print j
			if(prec == j) :
				count = count + 1
		#		print "COUNT"
				
			if(find != 0 and count == 2):
				offset = l.index(j)
				offset = offset - 4
				find = 0

		##	print j
			if(j != "0") :
				prec = j

		#print "TROUVE %d %s" % (offset, l.pop(offset))
		return offset
		
	def getTasksMemory(self) :
		""" Get tasks list by /dev/kmem or /dev/mem """
		
		current_addr = list_addr = 0
		name = ""
		
		self.mmemory.open("r", self.typeaccess)

		init_task = self.symbols.find_symbol("init_task")
		data = self.mmemory.read(init_task, 1000)
		self.offset_name = data.find("swapper")
		data = self.mmemory.read(init_task+40, 100)
		self.offset_list = self.getOffsetList(data)
		self.offset_list = self.offset_list * 4 + 40
		
		#print "OFFSET NAME %d" % self.offset_name
		#print "OFFSET LIST TASKS %d" % self.offset_list
		addr = unpack("<L", self.mmemory.read(init_task+self.offset_list, 4, 0))[0]
		data = self.mmemory.read(addr, 256, 0)
		self.offset_list_next = self.getOffsetListNext(data)
		#print "OFFSET LIST NEXT %d" % self.offset_list_next
		
		
		current_addr = unpack("<L", self.mmemory.read(addr + self.offset_list_next, 4, 0))[0]
		data = self.mmemory.read(current_addr+self.offset_list, 100, 0)

		self.offset_pid = self.getOffsetPid(data)
		#print "OFFSET PID %d" % self.offset_pid	
	
		data = self.mmemory.read(current_addr+self.offset_pid, 500, 0)

		self.offset_uid = self.getOffsetUid(data)
		#print "OFFSET UID %d" % self.offset_uid

		while(name != "swapper") :
			name = self.mmemory.read(current_addr + self.offset_name, 16, 0)
			name = name[:string.find(name, '\0')]
			
			pid = unpack("<L", self.mmemory.read(current_addr + self.offset_pid, 4, 0))[0]
			
			uid = unpack("<L", self.mmemory.read(current_addr + self.offset_uid, 4, 0))[0]
			gid = unpack("<L", self.mmemory.read(current_addr + self.offset_uid+16, 4, 0))[0]
			self.tasks_mem.map_tasks[int(pid)] = [int(uid), int(gid), name, current_addr, 0]
			self.tasks_mem.list_tasks.append(int(pid))
			
			list_addr = unpack("<L", self.mmemory.read(current_addr + self.offset_list, 4, 0))[0]

			current_addr = unpack("<L", self.mmemory.read(list_addr + self.offset_list_next, 4, 0))[0]

		self.tasks_mem.map_tasks.pop(0)
		self.tasks_mem.list_tasks.pop()

		self.mmemory.close()

	def getTasksPs(self) :
		""" Get tasks list by /bin/ps """
		
		i, o = os.popen2('/bin/ps -eo user,pid,ruid,rgid,state,comm')
		j = o.readline()
		j = o.readline()
		while(j != ""):
			l = j.split()
			self.tasks_ps.map_tasks[int(l[1])] = [int(l[2]), int(l[3]), l[5], 0, 0]
			self.tasks_ps.list_tasks.append(int(l[1]))
			j = o.readline()

		o.close()
		i.close()
				
	def openProcTaskStatus(self, file) :
		fd = 0
		
		try :
			fd = open(file, "r")
		except IOError :
			return [] 

		l = fd.readlines()
		name = l[0].split()
		pid = l[4].split()
		uid = l[7].split()
		gid = l[8].split()
		fd.close()			
	
		return [pid[1], uid[1], gid[1], name[1]]
		
	def getTasksProc(self) :
		""" Get tasks list by /proc """
		
		for rep in os.walk("/proc"):
			if(rep[0][6:].isdigit()):
				l = self.openProcTaskStatus(rep[0] + "/status")
				self.tasks_proc.map_tasks[int(l[0])] = [int(l[1]), int(l[2]), l[3], 0, 0]
				self.tasks_proc.list_tasks.append(int(l[0]))
				
				if(os.access(rep[0] + "/task", os.F_OK) == True):
					for srep in os.listdir(rep[0] + "/task"):
						if(srep != l[0]):
							ll = self.openProcTaskStatus(rep[0] + "/task/" + srep + "/status")
							self.tasks_proc.map_tasks[int(ll[0])] = [int(ll[1]), int(ll[2]), ll[3], 0, 1]
							self.tasks_proc.list_tasks.append(int(ll[0]))
				

	def getTasksProcForce(self) :
		""" Get tasks list by bruteforcing /proc """
		
		for i in range(1, 65535, 1) :
			if(os.access("/proc/" + str(i) + "/status", os.F_OK) == True):
				l = self.openProcTaskStatus("/proc/" + str(i) + "/status")
				if(l != []):
					self.tasks_procforce.map_tasks[int(l[0])] = [int(l[1]), int(l[2]), l[3], 0, 0]
					self.tasks_procforce.list_tasks.append(int(l[0]))			
					
					if(os.access("/proc/" + str(i) + "/task", os.F_OK) == True):
						for srep in os.listdir("/proc/" + str(i) + "/task"):
							if(srep != l[0]):
								ll = self.openProcTaskStatus("/proc/" + str(i) + "/task/" + srep + "/status")
								self.tasks_procforce.map_tasks[int(ll[0])] = [int(ll[1]), int(ll[2]), ll[3], 0, 1]
								self.tasks_procforce.list_tasks.append(int(ll[0]))
						
				
	def getTasksKill(self) :
		""" Get tasks list by kill """
		
		for i in range(1, 65535) :
			try :
				os.kill(i, 0)
				self.tasks_kill.map_tasks[i] = [0, 0, None, 0, 0]
				self.tasks_kill.list_tasks.append(i)

			except OSError :
				None

	def _simpleViewTasks(self, tasks) :
		print "PID\t UID\t GID\t NAME\t\t\t ADDR"

		for i in tasks.list_tasks:
			print "%d\t %d\t %d\t %-16s\t @ 0x%x" % (i, tasks.map_tasks[i][0], tasks.map_tasks[i][1], tasks.map_tasks[i][2], tasks.map_tasks[i][3])

	def viewTasks(self) :
		self.getTasksMemory()
		self._simpleViewTasks(self.tasks_mem)

	def _checkTasks(self, ref, cmp, check) :
		for i in ref.map_tasks :
			if(cmp.map_tasks.has_key(i) == False and ref.map_tasks[i][4] == 0):
				if(self.tasks_check.map_tasks.has_key(i) == False):
					check.map_tasks[i] = ref.map_tasks.get(i)
					check.list_tasks.append(i)
	
	def checkViewTasks(self) :
		self.getTasksPs()
		self.getTasksProc()
		self.getTasksProcForce()
		self.getTasksMemory()
		self.getTasksKill()

		self._checkTasks(self.tasks_proc, self.tasks_ps, self.tasks_check)
		self._checkTasks(self.tasks_procforce, self.tasks_proc, self.tasks_check)
		self._checkTasks(self.tasks_mem, self.tasks_procforce, self.tasks_check)
		self._checkTasks(self.tasks_kill, self.tasks_proc, self.tasks_check)
		
		if(self.tasks_check.list_tasks != []) :
			print "LISTS OF TASKS HIDE"
			self._simpleViewTasks(self.tasks_check)
		else :
			print "NO TASKS HIDE"
			print "YOUR SYSTEM SEEMS BE SAFE !"
