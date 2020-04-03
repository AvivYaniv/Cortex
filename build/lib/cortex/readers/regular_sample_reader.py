from cortex.readers.file_reader import FileReaderBase

from cortex.sample import Sample

class BinarySampleReader(FileReaderBase):
	
	version = 'binary'
	
	def __init__(self, file_path):
		super().__init__(file_path)
		self.generator      = Sample.read(self.stream)
			
	def read_user_information(self):
		return next(self.generator)
	
	def read_snapshot(self):
		return next(self.generator)
