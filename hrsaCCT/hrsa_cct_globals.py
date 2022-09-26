import logging
from logging.handlers import SocketHandler

# Attach Visual Log Viewer - cutelog
log = logging.getLogger('HRSA CCT Log')
log.setLevel(1)  # to send all records to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

# Global Variables
default_language_code = "en-US"
none_language_code = '(none)'

language_list = [
    '(none)',
    'en-US',
    'es-US'
]

audio_generation_language_list = [
    '(none)',
    'en-US',
    'es-US',
    'es-ES'
]

option_text_prefixes = [
    'A',
    'B',
    'C',
    'D',
    'E',
    '1',
    '2',
    '3',
    '4',
    '5',
]

dialogue_regular_expression = r"\".*?\""
option_regular_expression = r"[*](.*)\[(.*?(?=`))`(.*?(?=`))`(.*?(?=`))`(.*?(?=`|\]))(?:`(.*)])?"
option_display_text_regular_expression = r"\s*[A-Za-z0-9]+\s*[\.](.*)"
