
import pytest

from tests.test_constants import SERVER_MESSAGES_IDS
from tests.test_constants import PARSER_TYPES
from tests.test_constants import SAVER_MOCK_DEFAULT_IDS

from tests.test_constants import SAVER_SERVICE_TYPE
from tests.test_constants import PARSER_SERVICE_TYPE

from tests._utils.dictionary_file import DictionaryFile
from tests._utils.structured_file import StructuredFile

from tests.test_constants import get_message_queue_serivce_outputs_file_path

def test_parsers():
    parser_dictionay_file       = DictionaryFile(get_message_queue_serivce_outputs_file_path(PARSER_SERVICE_TYPE))
    parsed_output_dictionary    = parser_dictionay_file.read_dictionary()
    for parser_type in PARSER_TYPES:
        parsed_messages_by_current_parser_type = parsed_output_dictionary.get(parser_type, None)
        assert parsed_messages_by_current_parser_type is not None, f'Parser {parser_type} not configured'
        for message_id in SERVER_MESSAGES_IDS:
            assert message_id in parsed_messages_by_current_parser_type, f'Parser {parser_type} missed message {message_id}'
    
def convert_saved_lists_to_structure(saved_structure_lists):
    """
        Gets lines of savers output
        converts to following dictionaries:
            Foreach message -> savers and parsers
                <message_id> : [ <saver_id> : [ <parser_type>, ... , <parser_type> ] ]            
    """
    saved_structure             = {}
    for saved_structure_list in saved_structure_lists:
        message_id              = saved_structure_list[2]
        message_structure       = saved_structure.get(message_id, None)
        if not message_structure:
            saved_structure[message_id] = {}
        saver_id                = saved_structure_list[0]    
        saver_structure         = saved_structure[message_id]
        parser_structure        = saver_structure.get(saver_id, None)
        if not parser_structure:
            saver_structure[saver_id] = []
        parser_type             = saved_structure_list[1]
        saver_structure[saver_id].append(parser_type)
    return saved_structure
    
def test_savers():
    saver_structure_file        = StructuredFile(get_message_queue_serivce_outputs_file_path(SAVER_SERVICE_TYPE))
    saved_structure_lists       = saver_structure_file.read_lines()
    saved_structure             = convert_saved_lists_to_structure(saved_structure_lists)
    for messsage_id in SERVER_MESSAGES_IDS:
        message_structure       = saved_structure.get(messsage_id, None)
        assert message_structure is not None, f'Message {messsage_id} not saved'
        savers_for_message      = list(message_structure.keys())
        assert 1 == len(savers_for_message), f'Message {messsage_id} saved more than once!'
        saver_id                = savers_for_message[0]
        parsers_structure       = message_structure[saver_id]
        for parser_type in PARSER_TYPES:
            assert parser_type in parsers_structure, f'Message {messsage_id} not received from {parser_type}'
    
def test_savers_round_robin():
    saver_structure_file        = StructuredFile(get_message_queue_serivce_outputs_file_path(SAVER_SERVICE_TYPE))
    saved_structure_lists       = saver_structure_file.read_lines()
    saved_structure             = convert_saved_lists_to_structure(saved_structure_lists)
    savers_load_dictionary       = {}
    for messsage_id in SERVER_MESSAGES_IDS:
        message_structure       = saved_structure.get(messsage_id, None)
        assert message_structure is not None, f'Message {messsage_id} not saved'
        savers_for_message      = list(message_structure.keys())
        saver_id                = savers_for_message[0]
        saver_load              = savers_load_dictionary.get(saver_id, None)
        if not saver_load:
            savers_load_dictionary[saver_id] = []
        savers_load_dictionary[saver_id].append(messsage_id)
    loads = [ len(l) for l in list(savers_load_dictionary.values())]
    assert 1 == len(set(loads)), 'Savers load is not balanced'
    