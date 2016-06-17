#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import json
import urllib
import urllib2
import requests
import param

class Autoinj(object):
	"""
		sqlmapapi 接口建立和管理sqlmap任务
	"""

	def __init__(self, server='', target='', method='', data='', cookie='', referer=''):
		super(Autoinj, self).__init__()
		self.server = server
		if self.server[-1] != '/':
			self.server = self.server + '/'
		if method == "GET":
			self.target = target + '?' + data
		else:
			self.target = target
		self.taskid = ''
		self.engineid = ''
		self.status = ''
		self.method = method
		self.data = ''
		self.referer = referer
		self.cookie = cookie
		self.start_time = time.time()
		# print "server: %s \ttarget:%s \tmethod:%s \tdata:%s \tcookie:%s" % (self.server, self.target, self.method, self.data, self.cookie)

	#scan new task
	def task_new(self):
		code = urllib.urlopen(self.server + param.task_new).read()
		self.taskid = json.loads(code)['taskid']
		return True
	#delete scan task
	def task_delete(self):
		url = self.server + param.task_del
		url = url.replace(param.taskid, self.taskid)
		requests.get(url).json()
	#start scan task
	def scan_start(self):
		headers = {'Content-Type':'application/json'}
		print "starting to scan:\t" + '[',self.target,']' + "......"
		url = self.server + param.scan_task_start
		url = url.replace(param.taskid, self.taskid)
		data = {'url':self.target}
		t = requests.post(url, data=json.dumps(data), headers=headers).text
		t = json.loads(t)
		self.engineid = t['engineid']
		return True

	def scan_status(self):
		url = self.server + param.scan_task_status
		url = url.replace(param.taskid, self.taskid)
		self.status = requests.get(url).json()['status']

	def scan_data(self):
		url = self.server + param.scan_task_data
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def option_set(self):
		headers = {'Content-Type':'application/json'}
		url = self.server + param.option_task_set
		url = url.replace(param.taskid, self.taskid)
		data = {
				"user-agent":
					'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)
				 		AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106'''
				}

		if self.method == "POST":
			data["data"] = self.data
		if len(self.cookie)>1:
			data["cookie"] = self.cookie
		# print data

		t = requests.post(url, data=json.dumps(data), headers=headers).text
		t = json.loads(t)

	def option_get(self):
		url = self.server + param.option_task_get
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def scan_stop(self):
		url = self.server + param.scan_task_stop
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def scan_kill(self):
		url = self.server + param.scan_task_kill
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def run(self):
		# start task
		if not self.task_new():
			print "Error: task created failed."
			return False
		# set option var
		self.option_set()
		# start scan task
		if not self.scan_start():
			print "Error: scan start failed."
			return False
		# coding ..task scan
		while True:
			self.scan_status()
			if self.status == 'running':
				time.sleep(3)
			elif self.status== 'terminated':
				break
			else:
				print "unkown status"
				break
			if time.time() - self.start_time > 30000:
				error = True
				self.scan_stop()
				self.scan_kill()
				break

		# Result
		scan_res = self.scan_data()
		# delect task
		self.task_delete()
		print "耗时:" + str(time.time() - self.start_time)
		return scan_res

if __name__ == '__main__':
	server = 'http://127.0.0.1:8775/'
	with open('Scan_url.txt','r') as file:
		# data = "id=1"
		cookies = ""
		for target in file:
			inj = Autoinj(server,target,'GET',cookies)
			result = inj.run()
			print "Scan_Result",result
			print "\n================================================"
			if len(result['data'])>0:
				print "...存在SQL注入..."
			else:
				print "...not Injection..."