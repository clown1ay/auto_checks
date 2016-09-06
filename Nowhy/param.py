#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''sqlmapapi interface param'''

#User Methond's
task_new = "task/new"
task_del = "task/<taskid>/delete"

#Admin Functions
admin_task_list = "admin/<taskid>/list"
admin_task_flush = "admin/<taskid>/flush"

#Headler Task Option
option_task_list = "option/<taskid>/list"
option_task_get = "option/<taskid>/get"
option_task_set = "option/<taskid>/set"

#Scan Header
scan_task_start = "scan/<taskid>/start"
scan_task_stop = "scan/<taskid>/stop"
scan_task_kill = "scan/<taskid>/kill"
scan_task_status = "scan/<taskid>/status"
scan_task_data = "scan/<taskid>/data"

#Function's to headlers scans 'log
scan_task_log = "scan/<taskid>/log/<start>/<end>"
scan_task_log = "scan/<taskid>/log"

# Function to handle files inside the output directory
download = "download/<taskid>/<target>/<filename:path>"

#config
taskid = "<taskid>"


