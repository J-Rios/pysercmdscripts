# -*- coding: utf-8 -*-

'''
Script:
    texts.py
Description:
    Texts file
Author:
    Jose Miguel Rios Rubio
Date:
    22/03/2021
Version:
    1.0.0
'''

###############################################################################
### Texts

class TEXT():
    HELP = \
        "\n" \
        "NAME\n" \
        "       pysercmdscripts {}\n" \
        "\n" \
        "SYNOPSIS\n" \
        "       python pysercmdscripts.py [--help] [--version] " \
        "       [-f <CMD_FILE>]\n" \
        "\n" \
        "DESCRIPTION\n" \
        "       Python tool to automate send commands to a serial command " \
        "       line interface from a cmdscript text file that specify " \
        "       commands-responses with a simple language." \
        "\n" \
        "OPTIONS\n" \
        "       -h, --help\n" \
        "           Shows help text (current information).\n" \
        "\n" \
        "       -f --file\n" \
        "           Specify the cmdscript file to send commands.\n" \
        "\n" \
        "       -v, --version\n" \
        "           Shows current installed version.\n" \
        "\n" \
        "AUTHOR\n" \
        "       {}\n" \
        "\n" \
        "PROJECT REPOSITORY" \
        "       {}\n" \
        "\n" \
        "DONATION\n" \
        "       Do you like this program, buy me a coffee:\n" \
        "       {}\n" \
        "\n"

    OPT_FILE = \
        "\n" \
        "Specify the cmdscript file from where to send commands"

    IGNORE_OPTION = \
        "\n" \
        "Ignoring unkown option \"{}\"."

    BAD_OPTION = \
        "\n" \
        "Invalid arguments provided. Check --help information about usage."

    UNEXPECTED_CMDSCRIPT_CMD = \
        "Ignoring unkown command found in cmdscript: {}"

    INVALID_CMDSCRIPT_CMD = \
        "Ignoring invalid cmdscript command: {}"

    CMD_NO_ARGS = \
        "{} command without required arguments."

    CONNECT_INVALID_BAUDS = \
        "CONNECT command without valid baudrate"

    CONNECT_OPENING = \
        "CONNECT Opening Serial port {} at {} bauds..."

    CONNECT_OPEN_FAIL = \
        "CONNECT Can't open Serial port."

    CONNECT_OPEN = \
        "CONNECT Serial port open."

    DISCONNECT_CLOSE = \
        "DISCONNECT Serial port close."

    CFGEOL_INVALID = \
        "CFGEOL command without correct EOL value (CR, LF or CRLF)."

    CFGEOL_SET = \
        "CFGEOL End Of Line set to {}"

    CFGRESTIMEOUT_INVALID = \
        "CFGRESTIMEOUT command without correct time value (integer)."

    CFGRESTIMEOUT_SET = \
        "CFGRESTIMEOUT Response timeout set to {}ms"

    DELAY_INVALID = \
        "DELAY command without correct time value (integer)"

    DELAY = \
        "DELAY Waiting for {}s..."

    DELAYMS_INVALID = \
        "DELAYMS command without correct time value (integer)"

    DELAYMS = \
        "DELAYMS Waiting for {}ms..."

    CMD_SEND_FAIL = \
        "CMD Fail to send command: {}"

    CMD_SEND = \
        "CMD Send command: {}"

    RES_FAIL = \
        "RES Fail to receive expected response:\n" \
        "  Expected: {}\n" \
        "  Received: {}"

    RES_OK = \
        "RES Received expected response: {}"
