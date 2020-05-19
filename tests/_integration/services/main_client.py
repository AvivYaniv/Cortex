
import pathlib

from cortex.client import upload_sample

from cortex.readers.reader_versions import ReaderVersions

from tests.test_constants import project_root

if "__main__" == __name__:
    file_path = str(pathlib.Path(project_root(), 'example42.mind.gz'))
    host, port = '127.0.0.1', '8000'
    upload_sample(host, port, file_path=file_path, version=ReaderVersions.PROTOBUFF)
