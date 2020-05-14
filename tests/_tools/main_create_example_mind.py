
from cortex.readers import MindFileReader
from cortex.readers.reader_versions import ReaderVersions

# Change working directory to main directory
import os
from cortex.writers.mind.mind_writer import MindFileWriter
os.chdir('../../../')

# Constants Section
EXAMPLE_SNAPSHOTS_NUMBER    =   5
DEFAULT_FILE_PATH           =   'sample.mind.gz'
EXAMPLE_FILE_PATH           =   'example.mind.gz'
DEFAULT_FILE_VERSION        =   ReaderVersions.PROTOBUFF 
DEPRECTED_FILE_VERSION      =   [ ReaderVersions.BINARY ]   

def create_example_mind(file_path='', version=''):
    file_path           = file_path if file_path else DEFAULT_FILE_PATH
    version             = version if version else DEFAULT_FILE_VERSION
    
    if version in DEPRECTED_FILE_VERSION:
        print(f'ERROR! {version} is deprecated - won\'t export to example file')
        return
    
    with MindFileReader(file_path, version) as sample_reader:
        with MindFileWriter(EXAMPLE_FILE_PATH, version) as sample_writer:
            user_information     =     sample_reader.user_information
            sample_writer.write_user_information(user_information)            
            snapshots_counter = 0
            for snapshot in sample_reader:                
                snapshots_counter += 1
                sample_writer.write_snapshot(snapshot)
                if EXAMPLE_SNAPSHOTS_NUMBER == snapshots_counter:                    
                    break
        
    with MindFileReader(EXAMPLE_FILE_PATH, version) as sample_reader:
        user_information     =     sample_reader.user_information            
        snapshots_counter = 0
        for snapshot in sample_reader:                
            snapshots_counter += 1
            print(snapshots_counter)
        
    print(f'Exported {file_path} ---> {EXAMPLE_FILE_PATH} successfully!')
        
if "__main__" == __name__:
    create_example_mind()   
