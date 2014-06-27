# coding=UTF-8
import os
import sys
import csv
import arcpy
from Logger import Logger

class Exporter():
	
	def __init__(self):
		self.logger = Logger().getLogger(self.__class__.__name__)

	def exportToCSV(self, params):
		
		if(params.isValid()):
			try:
				self.logger.info('Starting process to export CSV file.')
				file = open(params.outputPath, 'wb')
				cursor = arcpy.da.SearchCursor(params.dataFeature, params.fields, params.where)
				writer = csv.writer(file, delimiter=params.delimiter, quotechar=params.quoteChar, quoting=csv.QUOTE_ALL)
				if (params.isHeader()):
					writer.writerow(params.header)
				for row in cursor:
					writer.writerow([s.encode('utf-8') if type(s) is unicode else s for s in row])
				file.close()
				self.logger.info('Finishing process to export CSV file.')
				return True
			except:
				if (file is not None):
					file.close()
				if (os.path.isfile(params.outputPath)):
					os.remove(params.outputPath)
				self.logger.error('Error to export feature to CSV. {0} - {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
				return False
		else:
			self.logger.error('Parameters are invalid to export feature to CSV.')
			return False
		
'''
Esta classe é responsável pelo tratamento dos parâmetros necessários 
para que seja exportado os dados de uma feature class, table ou table view.
'''
class Params(object):
	
	def __init__(self, dataFeature, path, filename):
		self.logger = Logger().getLogger(self.__class__.__name__)
		
		self._dataFeature = dataFeature
		self._path = path
		self._filename = filename
		self._outputPath = self._path +'\\'+ self._filename
		self._fields = '*'
		self._where = None
		self._delimiter = ','
		self._quoteChar = '"'
		self._header = self.header = self._fields

	@property
	def dataFeature(self):
		return self._dataFeature
		
	@property
	def path(self):
		return self._path
	
	@property	
	def filename(self):
		return self._filename
	
	@property
	def outputPath(self):
		return self._outputPath
		
	@property
	def fields(self):
		return self._fields
		
	@fields.setter
	def fields(self, fields):
		if(fields is not None and fields <> ''):
			self._fields = fields
			self._header = fields
	
	@property
	def where(self):
		return self._where
	
	@where.setter
	def where(self, where):
		self._where = where
	
	@property
	def delimiter(self):
		return self._delimiter
		
	@delimiter.setter
	def delimiter(self, delimiter):
		if(delimiter is not None and delimiter <> ''):
			self._delimiter = delimiter
	
	@property
	def quoteChar(self):
		return self._quoteChar
	
	@quoteChar.setter
	def quoteChar(self, quotechar):
		if(quotechar is not None and quotechar <> ''):
			self._quoteChar = quotechar
	
	@property
	def header(self):
		return self._header
	
	@header.setter
	def header(self, header):
		if(header <> '*'):
			self._header = header
		else:
			try:
				self._header = [f.aliasName for f in arcpy.ListFields(self._dataFeature)]
			except:
				self.logger.error('Error to create header. {0} - {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
				self._header = None
		
	def isHeader(self):
		if(self._header is not None and self._header <> ''):
			return True
		else:
			return False
		
	def isValid(self):
		if(self._dataFeature == None or self._dataFeature == ''):
			return False
		else:
			if not arcpy.Exists(self._dataFeature):
				self.logger.error('Error to access feature - {0}'.format(self._dataFeature))
				return False
		if(self._path == None or self._path == ''):
			return False
		else:
			try:
				if (not os.path.exists(self._path)):
					os.makedirs(self._path)
			except:
				self.logger.error('Error to create directory. {0} - {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
				return False
		if(self._filename == None or self._filename == ''):
			return False
		return True
