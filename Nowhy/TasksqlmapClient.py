#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
	SQLMapApi Scan Server:1270.0.0.1 Port:8775
	Time:2016/8/31
'''
import json
import requests
import param
import time
import config
try:
	import urllib
except ImportError:
	import urllib2

class SqlMclient(object):
	'''
	SQLMapApi Interface  > Task Client
	'''
	def __init__(self,server='',target='',method='',data='',cookie='',referer=''):
		super(SqlMclient,self).__init__()
		self.server = server
		if self.server[-1] != '/':
			self.server = self.server + '/'
		# if method == 'POST':
		# 	self.target = target + '?' + data
		# else:
		self.target = target
		self.taskid = ''
		self.data = data
		self.method = method
		self.engineid = ''
		self.status = ''
		self.cookie = cookie
		self.start_time = time.time()
		config.logger.info("[*]Conntent client sqlmapapi server[*]: %s" % config.API_URL)
	# new task start.
	def new_task(self):
		try:
			taskcode = urllib.urlopen(self.server + param.task_new).read()
			self.taskid = json.loads(taskcode)['taskid']
			# config.logger.info("[*]Create New TaskID[*]: %s" % self.taskid) New Task ID
			return True
		except IOError:
			config.logger.info("[*]Sqlmapapi.py is not running...[*]")
	# delete task [function]
	def del_task(self):
		url = self.server + param.task_del
		url = url.replace(param.taskid,self.taskid)
		del_code = requests.get(url).json()['success']
		# print "Del Task:",del_code
	# option param [function]
	def option_set(self):
		headers = {'Content-Type':'application/json'}
		url = self.server + param.option_task_set
		url = url.replace(param.taskid,self.taskid)
		# print requests.get(url).headers
		data = {"user-agent":
					'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)
				 		AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106''',
				# "smart":True,
				# "batch":True,
				# "getTables":True,
				"level":3,
				"risk":1
				# "purgeOutput":True
				}
		if self.method == "POST": data["data"] = self.data
		# print "Post data:",self.data  #id=1
		if len(self.cookie)>1: data["cookie"] = self.cookie
		# print "Cookit:",self.cookie
		send_res = requests.post(url,data=json.dumps(data),headers=headers).text
		# print json.loads(send_res) #.html.html
	# start scan task [function]
	def scan_start(self):
		headers = {'Content-Type':'application/json'}
		config.logger.info("[*]Start Scan Target URL[*]:... %s" % self.target)
		url = self.server + param.scan_task_start
		url = url.replace(param.taskid,self.taskid)
		data = {'url':self.target}
		send_res = requests.post(url,data=json.dumps(data),headers=headers).text
		send_res = json.loads(send_res)
		self.engineid = send_res['engineid']
		return True
	# get scan status [function]
	def scan_status(self):
		url = self.server + param.scan_task_status
		url = url.replace(param.taskid,self.taskid)
		self.status = requests.get(url).json()['status']
		# return self.status
	# get scan task Result [function]
	def scan_data(self):
		url = self.server + param.scan_task_data
		url = url.replace(param.taskid,self.taskid)
		return requests.get(url).json()
	# get option param [function]
	def option_get(self):
		url = self.server + param.option_task_get
		url = url.replace(param.taskid,self.taskid)
		return requests.get(url).json()
	# stop scan task [function]
	def scan_stop(self):
		url = self.server + param.scan_task_stop
		url = url.replace(param.taskid,self.taskid)
		return requests.get(url).json()
	# kill scan task [function]
	def scan_kill(self):
		url = self.server + param.scan_task_kill
		url = url.replace(param.taskid,self.taskid)
		return requests.get(url).json()

	#*****************************Main Function Run*****************************
	def run(self):
		#start Task.
		if not self.new_task():
			config.logger.info("[*]Error: Task failed.[*]")
			return False
		# option scan param.
		self.option_set()
		# run scan.
		if not self.scan_start():
			config.logger.info("[*]Error: Start scan Task failed[*]")
			return False
		#Waiting for the task to scan..
		while True:
			self.scan_status()

			if self.status == "running":
				time.sleep(3)
			elif self.status == "terminated":
				break
			else:
				config.logger.info("[!]Unkown Status[!]")
				break
			if time.time() - self.start_time > 500:  # > More 8
				error = True
				self.scan_stop()
				self.scan_kill()
				break
		result = self.scan_data()
		#delete Task
		self.del_task()

		# config.logger.info("[*]\t%s" % result)
		return result
		# time
		config.logger.info("[!]耗时:" + str(time.time()-self.start_time)+"秒[!]")



# if __name__ == '__main__':
# 	server = 'http://127.0.0.1:8775/'	
# 	target = "http://whw.rongchang.gov.cn/piclist.asp?id=0&key=1"
# 	# target = "http://www.gdzjnsd.com/nsdnew/Detailed.asp?ProductNO=571"
# 	data = ""
# 	cookie = 'Abve12UIYH344'
# 	scan = SqlMclient(server,target,'GET',data,cookie)
# 	res = scan.run()
# 	print res