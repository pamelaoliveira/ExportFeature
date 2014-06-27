# coding=UTF-8
import os
import logging
import logging.config
import log_config
from datetime import date

class Logger:
	
	def __init__(self):
		if (not os.path.exists(log_config.LOG_DIRECTORY)):
			os.makedirs(log_config.LOG_DIRECTORY)
			
		logfilename = log_config.LOG_DIRECTORY + "\\" + log_config.LOG_FILENAME + "_" + date.today().strftime("%Y_%m_%d") + ".log"
		logging.config.fileConfig(log_config.LOGGING, defaults={'logfilename': logfilename}, disable_existing_loggers=0)

	def getLogger(self, name):
		return logging.getLogger(name)
