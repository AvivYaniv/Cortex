
from cortex.readers import MindFileReader
from cortex.readers.reader_versions import ReaderVersions

from tests.test_constants import get_user_test_file_path
from tests.test_constants import get_test_user

from tests.test_constants import DEFAULT_FILE_VERSION

from cortex.writers.mind.mind_writer import MindFileWriter
from cortex.entities.user_feelings import UserFeelings

from cortex.utils import change_direcoty_to_project_root

# Constants Section
EXAMPLE_SNAPSHOTS_NUMBER        =   367
DEFAULT_FILE_PATH               =   'sample.mind.gz'

DEPRECTED_FILE_VERSION          =   [ ReaderVersions.BINARY ]   

class SNAPSHOT_MANIPULATOR_FLAGS:
    USER_FEELINGS_REVERSE       = 0
    DEPTH_IMAGE_SIZE_SWITCH     = 1

def snapshot_manipulator(snapshot, snapshot_manipulator_flags):
    if SNAPSHOT_MANIPULATOR_FLAGS.USER_FEELINGS_REVERSE in snapshot_manipulator_flags:
        original_feelings = snapshot.user_feelings 
        snapshot.user_feelings = UserFeelings(original_feelings.get()[::-1])
    if SNAPSHOT_MANIPULATOR_FLAGS.DEPTH_IMAGE_SIZE_SWITCH in snapshot_manipulator_flags:
        snapshot.depth_image.height, snapshot.depth_image.width = \
            snapshot.depth_image.width, snapshot.depth_image.height

@change_direcoty_to_project_root()
def create_test_mind_file(file_path='', version='', test_user_number=1, snapshot_manipulator_flags=None):
    file_path           = file_path if file_path else DEFAULT_FILE_PATH
    version             = version if version else DEFAULT_FILE_VERSION
    
    if version in DEPRECTED_FILE_VERSION:
        print(f'ERROR! {version} is deprecated - won\'t export to example file')
        return
    
    example_file_path = get_user_test_file_path(test_user_number)
    
    with MindFileReader(file_path, version) as sample_reader:
        with MindFileWriter(example_file_path, version) as sample_writer:
            user_information     =     sample_reader.user_information
            if test_user_number:
                user_information.user_id    = int(get_test_user(test_user_number).ID)
                user_information.username   = get_test_user(test_user_number).NAME              
            sample_writer.write_user_information(user_information)            
            snapshots_counter = 0
            for snapshot in sample_reader:                
                snapshots_counter += 1
                if snapshot_manipulator_flags:
                    snapshot_manipulator(snapshot, snapshot_manipulator_flags)
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
    create_test_mind_file(test_user_number              =   2,  \
                          snapshot_manipulator_flags    =       \
                            [ SNAPSHOT_MANIPULATOR_FLAGS.USER_FEELINGS_REVERSE, SNAPSHOT_MANIPULATOR_FLAGS.DEPTH_IMAGE_SIZE_SWITCH ])   
