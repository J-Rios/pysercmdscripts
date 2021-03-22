# -*- coding: utf-8 -*-

'''
Script:
    constants.py
Description:
    Constants file
Author:
    Jose Miguel Rios Rubio
Date:
    22/03/2021
Version:
    1.0.0
'''

###############################################################################
### Imported modules

from os import path as os_path

###############################################################################
### Constants

# Program return codes
class RC():
    OK = 0
    FAIL = -1


# Log available levels
class LOG():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


# End Of Line characters
class EOL():
    CR = '\r'
    LF = '\n'
    CRLF = '\r\n'


# Constants
class CONST():

    # Current Log level to use
    LOG_LEVEL = LOG.INFO

    # Log timestamp format
    LOG_TIMESTAMP_FORMAT = "%Y-%m-%d_%H:%M:%S"

    # Application Version
    APP_VERSION = "1.0.0 (22/03/2021)"

    # Main Developer
    AUTHOR = "Jose Miguel Rios Rubio"

    # Project code repository
    PROJECT_REPO = "https://github.com/J-Rios/pysercmdscripts"

    # Developer donation address
    DEV_DONATE = "https://www.paypal.com/paypalme/josrios"

    # Actual constants.py full path directory name
    SCRIPT_PATH = os_path.dirname(os_path.realpath(__file__))

    # Input arguments flags
    OPTIONS = \
    [
        "-h", "--help",
        "-f", "--file",
        "-v", "--version"
    ]

    # Supported cmdscript commands
    CMDSCRIPT_COMMANDS = \
    [
        "CONNECT", "DISCONNECT", "CFGEOL", "CFGRESTIMEOUT", "DELAY",
        "DELAYMS", "EOL", "CMD", "RES"
    ]

    # Common Serial BaudRates
    SERIAL_COMMON_BAUDS = \
    [
        115200, 19200, 9600, 1200, 2400, 4800,
        50, 75, 110, 134, 150, 200, 300, 600,
        1800, 19200, 38400, 57600, 230400,
        460800, 500000, 576000, 921600
    ]

    # Common human texts characters
    SERIAL_AUTODETECT_ASCII_LIST = \
    [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9'
    ]

