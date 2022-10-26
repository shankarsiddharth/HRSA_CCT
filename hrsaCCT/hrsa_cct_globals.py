import hrsa_logger

log = hrsa_logger.HRSALogger()

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
