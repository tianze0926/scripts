filebrowser = 'D:/Downloads/filebrowser/filebrowser.exe'
filebrowser_db = 'D:/Downloads/filebrowser/filebrowser.db'

import sys

if len(sys.argv) > 1:

	root_dir = sys.argv[1]
	filebrowser_cmd = f'{filebrowser} -d {filebrowser_db} -a 127.0.0.1 -p 54321 --noauth -r {root_dir}'

	frp = 'D:/Downloads/frp/frpc.exe'
	frp_config = 'D:/Downloads/frp/frpc.ini'
	frp_cmd = f'{frp} -c {frp_config}'

	import subprocess
	import threading

	processes = {}
	thread_lock = threading.Lock()

	class RunCommand(threading.Thread):
		def __init__(self, cmd, name):
			threading.Thread.__init__(self)
			self.cmd = cmd
			self.name = name
		def run(self):
			thread_lock.acquire()
			processes[self.name] = []
			thread_lock.release()
			process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
			while True:
				line = process.stdout.readline().decode()
				if line == '' and process.poll() is not None:
					break
				thread_lock.acquire()
				processes[self.name].append(line)
				thread_lock.release()

	thread_filebrowser = RunCommand(filebrowser_cmd, 'filebrowser')
	thread_frp = RunCommand(frp_cmd, 'frp')

	thread_filebrowser.start()
	thread_frp.start()

	old_processes = {}
	import time
	import copy
	from datetime import datetime
	while True:
		temp_processes = copy.deepcopy(processes)
		if old_processes != temp_processes:
			old_processes = temp_processes
			print(f'------------ {datetime.now()} ------------')
			print('[filebrowser]')
			for i in temp_processes['filebrowser']:
				print(i)
			print('[frp]')
			for i in temp_processes['frp']:
				print(i)
		
		time.sleep(1)

else:
	print('Error: No arguments provided')


