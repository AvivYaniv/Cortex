import gzip

class ProtobufSampleReader:
	
	version = 'v2'
	
	def __init__(self, file_path):
		self.stream = gzip(file_path, 'rb')
		
	def read_user_information(self):
		pass
	
	def read_snapshot(self):
		pass
