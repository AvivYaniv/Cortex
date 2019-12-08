import datetime as dt

import pytest

from cortex import Thought


user_id = 1
datetime = dt.datetime(2000, 1, 1, 12, 0)
thought = "I'm hungry"

import time
from struct import pack, calcsize

DATETIME_FORMAT                 = '%Y-%m-%d_%H:%M:%S'
    
THOUGHT_HEADER_FORMAT           = '<QQI'
HEADER_SIZE                     = calcsize(THOUGHT_HEADER_FORMAT)

def serialize(user_id, timestamp, thought):
        thought_size, thought_data      = len(thought), thought.encode('utf-8')
                
        # user_id        :    uint64
        # timestamp      :    uint64
        # thought_size   :    uint32
        # thought_data   :    <thought size> bytes
        THOUGHT_DATA_FORMAT             = '{0}s'.format(thought_size)
        THOUGHT_FORMAT                  = Thought.THOUGHT_HEADER_FORMAT + THOUGHT_DATA_FORMAT
         
        time_stamp_as_number = int(time.mktime(timestamp.timetuple()))
        
        return                          \
            pack(THOUGHT_FORMAT,        \
                 user_id,               \
                 time_stamp_as_number,  \
                 thought_size,          \
                 thought_data)

# To avoid machine dependant serialization
serialized = serialize(user_id, datetime, thought)

@pytest.fixture
def t():
    return Thought(user_id, datetime, thought)


def test_attributes(t):
    assert t.user_id == user_id
    assert t.timestamp == datetime
    assert t.thought == thought


def test_repr(t):
    assert repr(t) == f'Thought(user_id={user_id!r}, timestamp={datetime!r}, thought={thought!r})'


def test_str(t):
    assert str(t) == f'[{datetime:%Y-%m-%d_%H:%M:%S}] user {user_id}: {thought}'


def test_eq(t):
    t1 = Thought(user_id, datetime, thought)
    assert t1 == t
    t2 = Thought(user_id + 1, datetime, thought)
    assert t2 != t
    t3 = Thought(user_id, datetime + dt.timedelta(minutes=1), thought)
    assert t3 != t
    t4 = Thought(user_id, datetime, thought + '!')
    assert t4 != t
    t5 = 1
    assert t5 != t
    t6 = lambda: None
    t6.user_id = user_id
    t6.timestamp = datetime
    t6.thought = thought
    assert t6 != t


def test_serialize(t):
    assert t.serialize() == serialized


def test_deserialize(t):
    t = Thought.deserialize(serialized)
    assert t.user_id == user_id
    assert t.timestamp == datetime
    assert t.thought == thought


def test_symmetry(t):
    assert Thought.deserialize(t.serialize()) == t
