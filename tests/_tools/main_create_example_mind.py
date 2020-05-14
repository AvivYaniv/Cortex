
from cortex.readers import MindFileReader
from cortex.readers.reader_versions import ReaderVersions

from tests.test_constants import get_user_test_file_path
from tests.test_constants import TEST_USER_1_ID, TEST_USER_2_ID

# Change working directory to main directory
import os
from cortex.writers.mind.mind_writer import MindFileWriter
os.chdir('../../')

# Constants Section
EXAMPLE_SNAPSHOTS_NUMBER    =   5
DEFAULT_FILE_PATH           =   'sample.mind.gz'

DEFAULT_FILE_VERSION        =   ReaderVersions.PROTOBUFF 
DEPRECTED_FILE_VERSION      =   [ ReaderVersions.BINARY ]   

def create_example_mind(file_path='', version='', example_user_id=''):
    file_path           = file_path if file_path else DEFAULT_FILE_PATH
    version             = version if version else DEFAULT_FILE_VERSION
    
    if version in DEPRECTED_FILE_VERSION:
        print(f'ERROR! {version} is deprecated - won\'t export to example file')
        return
    
    example_file_path = get_user_test_file_path(example_user_id)
    
    with MindFileReader(file_path, version) as sample_reader:
        with MindFileWriter(example_file_path, version) as sample_writer:
            user_information     =     sample_reader.user_information
            if example_user_id:
                user_information.user_id = int(example_user_id)
            sample_writer.write_user_information(user_information)            
            snapshots_counter = 0
            for snapshot in sample_reader:                
                snapshots_counter += 1
                sample_writer.write_snapshot(snapshot)
                if EXAMPLE_SNAPSHOTS_NUMBER == snapshots_counter:                    
                    break
        
    with MindFileReader(example_file_path, version) as sample_reader:
        user_information     =     sample_reader.user_information            
        snapshots_counter = 0
        for snapshot in sample_reader:                
            snapshots_counter += 1
            
    assert EXAMPLE_SNAPSHOTS_NUMBER == snapshots_counter 
        
    print(f'Exported {file_path} ---> {example_file_path} successfully!')
        
if "__main__" == __name__:
    create_example_mind(example_user_id=TEST_USER_1_ID)   
