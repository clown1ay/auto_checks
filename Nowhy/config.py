#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Config # sqlmapapi server | logging option
'''
import logging
import sys
import subprocess as subpro

API_URL = 'http://127.0.0.1:8775'

# subpro.Popen('sqlmap-master/sqlmapapi.py -s',shell=True)

LEVELS = {
	'debug':logging.DEBUG,
	'info':logging.INFO,
	'warning':logging.WARNING,
	'error':logging.ERROR,
	'critical':logging.CRITICAL
}

LOG = {
	"levle":LEVELS['debug'],
	"filename":"sqlmclient",
	"format":'[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s',
	"datefmt":'%Y-%m-%d %H:%M:%S'
}

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(LEVELS['debug'])
logger.setLevel(LEVELS['info'])
