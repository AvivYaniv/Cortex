import os.path

from cortex.readers import MindFileReader

from cortex.utils import Connection

from cortex.protocol import ProtocolMessagesTyeps, Protocol

from cortex.readers.reader_versions import ReaderVersions

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
DEFAULT_HOST            =    '127.0.0.1'
DEFAULT_PORT            =    '8000'
DEFAULT_FILE_PATH       =    'sample.mind.gz'
DEFAULT_FILE_VERSION    =    ReaderVersions.PROTOBUFF

# Setting default protocol    
protocol = Protocol() 

class ClientService:
    # Constructor Section
    def __init__(self, host='', port=''):
        """Sends to the server user's sample file"""
        # Default parameter resolution
        self.total_snapshots_uploaded   = 0
        self.server_ip_str              = host if host else DEFAULT_HOST
        self.server_port_int            = int(port if port else DEFAULT_PORT)
    # Methods Section
    # Sends hello message to server
    def send_hello_message(self, user_information):
        hello_message = protocol.get_message(ProtocolMessagesTyeps.HELLO_MESSAGE)(user_information)
        try:
            self.connection.send_message(hello_message.serialize())
        except Exception as e:
            # TODO DEBUG REMOVE
            emsg = str(e)            
            if "[Errno 1]" in emsg:
                return "EPERM    Operation not permitted"
            if "[Errno 2]" in emsg:
                return "ENOENT    No such file or directory"
            if "[Errno 3]" in emsg:
                return "ESRCH    No such process"
            if "[Errno 4]" in emsg:
                return "EINTR    Interrupted system call"
            if "[Errno 5]" in emsg:
                return "EIO    I/O error"
            if "[Errno 6]" in emsg:
                return "ENXIO    No such device or address"
            if "[Errno 7]" in emsg:
                return "E2BIG    Argument list too long"
            if "[Errno 8]" in emsg:
                return "ENOEXEC    Exec format error"
            if "[Errno 9]" in emsg:
                return "EBADF    Bad file number"
            if "[Errno 10]" in emsg:
                return "ECHILD    No child processes"
            if "[Errno 11]" in emsg:
                return "EAGAIN    Try again"
            if "[Errno 12]" in emsg:
                return "ENOMEM    Out of memory"
            if "[Errno 13]" in emsg:
                return "EACCES    Permission denied"
            if "[Errno 14]" in emsg:
                return "EFAULT    Bad address"
            if "[Errno 15]" in emsg:
                return "ENOTBLK    Block device required"
            if "[Errno 16]" in emsg:
                return "EBUSY    Device or resource busy"
            if "[Errno 17]" in emsg:
                return "EEXIST    File exists"
            if "[Errno 18]" in emsg:
                return "EXDEV    Cross-device link"
            if "[Errno 19]" in emsg:
                return "ENODEV    No such device"
            if "[Errno 20]" in emsg:
                return "ENOTDIR    Not a directory"
            if "[Errno 21]" in emsg:
                return "EISDIR    Is a directory"
            if "[Errno 22]" in emsg:
                return "EINVAL    Invalid argument"
            if "[Errno 23]" in emsg:
                return "ENFILE    File table overflow"
            if "[Errno 24]" in emsg:
                return "EMFILE    Too many open files"
            if "[Errno 25]" in emsg:
                return "ENOTTY    Not a typewriter"
            if "[Errno 26]" in emsg:
                return "ETXTBSY    Text file busy"
            if "[Errno 27]" in emsg:
                return "EFBIG    File too large"
            if "[Errno 28]" in emsg:
                return "ENOSPC    No space left on device"
            if "[Errno 29]" in emsg:
                return "ESPIPE    Illegal seek"
            if "[Errno 30]" in emsg:
                return "EROFS    Read-only file system"
            if "[Errno 31]" in emsg:
                return "EMLINK    Too many links"
            if "[Errno 32]" in emsg:
                return "EPIPE    Broken pipe"
            if "[Errno 33]" in emsg:
                return "EDOM    Math argument out of domain of func"
            if "[Errno 34]" in emsg:
                return "ERANGE    Math result not representable"
            if "[Errno 35]" in emsg:
                return "EDEADLK    Resource deadlock would occur"
            if "[Errno 36]" in emsg:
                return "ENAMETOOLONG    File name too long"
            if "[Errno 37]" in emsg:
                return "ENOLCK    No record locks available"
            if "[Errno 38]" in emsg:
                return "ENOSYS    Function not implemented"
            if "[Errno 39]" in emsg:
                return "ENOTEMPTY    Directory not empty"
            if "[Errno 40]" in emsg:
                return "ELOOP    Too many symbolic links encountered"
            if "[Errno 42]" in emsg:
                return "ENOMSG    No message of desired type"
            if "[Errno 43]" in emsg:
                return "EIDRM    Identifier removed"
            if "[Errno 44]" in emsg:
                return "ECHRNG    Channel number out of range"
            if "[Errno 45]" in emsg:
                return "EL2NSYNC    Level 2 not synchronized"
            if "[Errno 46]" in emsg:
                return "EL3HLT    Level 3 halted"
            if "[Errno 47]" in emsg:
                return "EL3RST    Level 3 reset"
            if "[Errno 48]" in emsg:
                return "ELNRNG    Link number out of range"
            if "[Errno 49]" in emsg:
                return "EUNATCH    Protocol driver not attached"
            if "[Errno 50]" in emsg:
                return "ENOCSI    No CSI structure available"
            if "[Errno 51]" in emsg:
                return "EL2HLT    Level 2 halted"
            if "[Errno 52]" in emsg:
                return "EBADE    Invalid exchange"
            if "[Errno 53]" in emsg:
                return "EBADR    Invalid request descriptor"
            if "[Errno 54]" in emsg:
                return "EXFULL    Exchange full"
            if "[Errno 55]" in emsg:
                return "ENOANO    No anode"
            if "[Errno 56]" in emsg:
                return "EBADRQC    Invalid request code"
            if "[Errno 57]" in emsg:
                return "EBADSLT    Invalid slot"
            if "[Errno 59]" in emsg:
                return "EBFONT    Bad font file format"
            if "[Errno 60]" in emsg:
                return "ENOSTR    Device not a stream"
            if "[Errno 61]" in emsg:
                return "ENODATA    No data available"
            if "[Errno 62]" in emsg:
                return "ETIME    Timer expired"
            if "[Errno 63]" in emsg:
                return "ENOSR    Out of streams resources"
            if "[Errno 64]" in emsg:
                return "ENONET    Machine is not on the network"
            if "[Errno 65]" in emsg:
                return "ENOPKG    Package not installed"
            if "[Errno 66]" in emsg:
                return "EREMOTE    Object is remote"
            if "[Errno 67]" in emsg:
                return "ENOLINK    Link has been severed"
            if "[Errno 68]" in emsg:
                return "EADV    Advertise error"
            if "[Errno 69]" in emsg:
                return "ESRMNT    Srmount error"
            if "[Errno 70]" in emsg:
                return "ECOMM    Communication error on send"
            if "[Errno 71]" in emsg:
                return "EPROTO    Protocol error"
            if "[Errno 72]" in emsg:
                return "EMULTIHOP    Multihop attempted"
            if "[Errno 73]" in emsg:
                return "EDOTDOT    RFS specific error"
            if "[Errno 74]" in emsg:
                return "EBADMSG    Not a data message"
            if "[Errno 75]" in emsg:
                return "EOVERFLOW    Value too large for defined data type"
            if "[Errno 76]" in emsg:
                return "ENOTUNIQ    Name not unique on network"
            if "[Errno 77]" in emsg:
                return "EBADFD    File descriptor in bad state"
            if "[Errno 78]" in emsg:
                return "EREMCHG    Remote address changed"
            if "[Errno 79]" in emsg:
                return "ELIBACC    Can not access a needed shared library"
            if "[Errno 80]" in emsg:
                return "ELIBBAD    Accessing a corrupted shared library"
            if "[Errno 81]" in emsg:
                return "ELIBSCN    .lib section in a.out corrupted"
            if "[Errno 82]" in emsg:
                return "ELIBMAX    Attempting to link in too many shared libraries"
            if "[Errno 83]" in emsg:
                return "ELIBEXEC    Cannot exec a shared library directly"
            if "[Errno 84]" in emsg:
                return "EILSEQ    Illegal byte sequence"
            if "[Errno 85]" in emsg:
                return "ERESTART    Interrupted system call should be restarted"
            if "[Errno 86]" in emsg:
                return "ESTRPIPE    Streams pipe error"
            if "[Errno 87]" in emsg:
                return "EUSERS    Too many users"
            if "[Errno 88]" in emsg:
                return "ENOTSOCK    Socket operation on non-socket"
            if "[Errno 89]" in emsg:
                return "EDESTADDRREQ    Destination address required"
            if "[Errno 90]" in emsg:
                return "EMSGSIZE    Message too long"
            if "[Errno 91]" in emsg:
                return "EPROTOTYPE    Protocol wrong type for socket"
            if "[Errno 92]" in emsg:
                return "ENOPROTOOPT    Protocol not available"
            if "[Errno 93]" in emsg:
                return "EPROTONOSUPPORT    Protocol not supported"
            if "[Errno 94]" in emsg:
                return "ESOCKTNOSUPPORT    Socket type not supported"
            if "[Errno 95]" in emsg:
                return "EOPNOTSUPP    Operation not supported on transport endpoint"
            if "[Errno 96]" in emsg:
                return "EPFNOSUPPORT    Protocol family not supported"
            if "[Errno 97]" in emsg:
                return "EAFNOSUPPORT    Address family not supported by protocol"
            if "[Errno 98]" in emsg:
                return "EADDRINUSE    Address already in use"
            if "[Errno 99]" in emsg:
                return "EADDRNOTAVAIL    Cannot assign requested address"
            if "[Errno 100]" in emsg:
                return "ENETDOWN    Network is down"
            if "[Errno 101]" in emsg:
                return "ENETUNREACH    Network is unreachable"
            if "[Errno 102]" in emsg:
                return "ENETRESET    Network dropped connection because of reset"
            if "[Errno 103]" in emsg:
                return "ECONNABORTED    Software caused connection abort"
            if "[Errno 104]" in emsg:
                return "ECONNRESET    Connection reset by peer"
            if "[Errno 105]" in emsg:
                return "ENOBUFS    No buffer space available"
            if "[Errno 106]" in emsg:
                return "EISCONN    Transport endpoint is already connected"
            if "[Errno 107]" in emsg:
                return "ENOTCONN    Transport endpoint is not connected"
            if "[Errno 108]" in emsg:
                return "ESHUTDOWN    Cannot send after transport endpoint shutdown"
            if "[Errno 109]" in emsg:
                return "ETOOMANYREFS    Too many references: cannot splice"
            if "[Errno 110]" in emsg:
                return "ETIMEDOUT    Connection timed out"
            if "[Errno 111]" in emsg:
                return "ECONNREFUSED    Connection refused"
            if "[Errno 112]" in emsg:
                return "EHOSTDOWN    Host is down"
            if "[Errno 113]" in emsg:
                return "EHOSTUNREACH    No route to host"
            if "[Errno 114]" in emsg:
                return "EALREADY    Operation already in progress"
            if "[Errno 115]" in emsg:
                return "EINPROGRESS    Operation now in progress"
            if "[Errno 116]" in emsg:
                return "ESTALE    Stale NFS file handle"
            if "[Errno 117]" in emsg:
                return "EUCLEAN    Structure needs cleaning"
            if "[Errno 118]" in emsg:
                return "ENOTNAM    Not a XENIX named type file"
            if "[Errno 119]" in emsg:
                return "ENAVAIL    No XENIX semaphores available"
            if "[Errno 120]" in emsg:
                return "EISNAM    Is a named type file"
            if "[Errno 121]" in emsg:
                return "EREMOTEIO    Remote I/O error"
            if "[Errno 122]" in emsg:
                return "EDQUOT    Quota exceeded"
            if "[Errno 123]" in emsg:
                return "ENOMEDIUM    No medium found"
            if "[Errno 124]" in emsg:
                return "EMEDIUMTYPE    Wrong medium type"
            if "[Errno 125]" in emsg:
                return "ECANCELED    Operation Canceled"
            if "[Errno 126]" in emsg:
                return "ENOKEY    Required key not available"
            if "[Errno 127]" in emsg:
                return "EKEYEXPIRED    Key has expired"
            if "[Errno 128]" in emsg:
                return "EKEYREVOKED    Key has been revoked"
            if "[Errno 129]" in emsg:
                return "EKEYREJECTED    Key was rejected by service"
            if "[Errno 130]" in emsg:
                return "EOWNERDEAD    Owner died"
            if "[Errno 131]" in emsg:
                return "ENOTRECOVERABLE    State not recoverable"
            # TODO DEBUG REMOVE            
            logger.error(f'error while sending hello_message: {e}')            
            self._is_valid_connection = False
            return
    # Receives configuration message from server
    def receive_config_message(self):
        try:
            config_message_bytes           = self.connection.receive_message()
        except Exception as e:
            logger.error(f'error receiving config_message : {e}')
            self._is_valid_connection   = False
            return None
        try:
            config_message                 = protocol.get_message(ProtocolMessagesTyeps.CONFIG_MESSAGE).read(config_message_bytes)
        except Exception as e:
            # TODO DEBUG REMOVE
            raise e
            # TODO DEBUG REMOVE
            logger.error(f'error while parsing config_message: {e}')
            self._is_valid_connection     = False
            return None
        return config_message
    # Sends snapshot message to server
    def send_snapshot_message(self, snapshot, fields):
        snapshot_message = protocol.get_message(ProtocolMessagesTyeps.SNAPSHOT_MESSAGE)(snapshot, fields)
        try:
            self.connection.send_message(snapshot_message.serialize())
            self.total_snapshots_uploaded   += 1
        except Exception as e:
            logger.error(f'error while sending snapshot_message: {e}')
            self._is_valid_connection = False
            return
    # Uploads a mind file to server    
    def upload_sample(self, file_path='', version=''):
        file_path     = file_path if file_path else DEFAULT_FILE_PATH
        version     = version if version else DEFAULT_FILE_VERSION
        # Logging initialization
        logger.info(f'initializing client to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')
        # Validating sample file exists - else quitting
        if not os.path.isfile(file_path):
            logger.error(f'sample file not found at path {file_path}')
            return
        # Initializing connection status as valid
        self._is_valid_connection = True        
        # Reading mind file and sending it to server    
        with MindFileReader(file_path, version) as sample_reader:
            with Connection.connect(self.server_ip_str, self.server_port_int) as connection:                    
                self.connection      =      connection
                # Sending hello message
                user_information     =      sample_reader.user_information                
                self.send_hello_message(user_information)
                if not self._is_valid_connection:
                    return
                # Receiving configuration message
                config_message = self.receive_config_message()
                if not self._is_valid_connection:
                    return
                fields = config_message.fields            
                # Sending snapshot messages
                for snapshot in sample_reader:                    
                    self.send_snapshot_message(snapshot, fields)
                    if not self._is_valid_connection:
                        return
        # Logging client has finished to upload file
        print(f'client has finished to upload {file_path} of version {version} to server at {self.server_ip_str}:{self.server_port_int}')

def upload_sample(host='', port='', file_path='', version=''):
    client_service = ClientService(host, port)
    client_service.upload_sample(file_path, version)
