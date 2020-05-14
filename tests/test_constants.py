
# User Section
TEST_USER_1_ID                          =   '42'
TEST_USER_2_ID                          =   '100'

# Durations Section
SERVER_SNAPSHOT_MAX_DURATION_HANDLING   =   1

# Hosts
SERVER_TEST_HOST                        =   '0.0.0.0'

# File names
EXAMPLE_FILE_PATH_FORMAT                =   'example%s.mind.gz'

def get_user_test_file_path(user_id):
    return EXAMPLE_FILE_PATH_FORMAT % user_id
