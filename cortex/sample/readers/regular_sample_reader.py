import io

from ..sample import Sample

class RegularSampleReader:
	
	version = 'v1'
	
	def __init__(self, file_path):
		self.stream         = io.open(file_path, mode='rb')
		self.generator      = Sample.read(self.stream)
		
	def read_user_information(self):
		return next(self.generator)
	
	def read_snapshot(self):
		return next(self.generator)
