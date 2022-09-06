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
