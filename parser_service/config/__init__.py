import os

LANGUAGE_SYTAX_DIRECTORY = 'parser_service/config/language_syntax'

LANGUAGE_SYNTAX = {}


for filename in os.listdir(LANGUAGE_SYTAX_DIRECTORY):
    if filename.endswith('.syntax'):
        LANGUAGE_SYNTAX[filename[0:-7]] = open(os.path.join(LANGUAGE_SYTAX_DIRECTORY, filename)).readlines()

