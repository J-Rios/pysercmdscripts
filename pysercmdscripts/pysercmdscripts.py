#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    pysercmdscripts.py
Description:
    Python tool to automate send commands to a serial command line interface 
    from a *cmdscript* text file that specify commands-responses with a 
    simple language.
Author:
    Jose Miguel Rios Rubio
Date:
    22/03/2021
Version:
    1.0.0
'''

###############################################################################
### Imported modules

from sys import argv as sys_argv
from sys import exit as sys_exit
from argparse import ArgumentParser as argparse_ArgumentParser
from time import sleep

from constants import RC, LOG, EOL, CONST
from texts import TEXT
from auxiliar import print_log, is_int
from filesrw import file_read_all_text
from serialcomm import (
    serial_open, serial_close, serial_read, serial_read_str,
    serial_read_until, serial_write
)

###############################################################################
### Globals

eol = EOL.CR
res_timeout = 1.0
ser = None
th_read = None
th_write = None
g_terminal_close = False

###############################################################################
### Input Arguments Functions

def show_help():
    '''Print to stdout program usage help info.'''
    text_help = TEXT.HELP.format(
                    CONST.APP_VERSION, CONST.AUTHOR,
                    CONST.PROJECT_REPO, CONST.DEV_DONATE
                )
    print(LOG.INFO, text_help)


def parse_options():
    '''Get and parse program input arguments.'''
    arg_parser = argparse_ArgumentParser()
    arg_parser.version = CONST.APP_VERSION
    arg_parser.add_argument("file", help=TEXT.OPT_FILE, action='store',
            nargs=1, type=str)
    arg_parser.add_argument("-v", "--version", action='version')
    args = arg_parser.parse_args()
    return vars(args)

###############################################################################
### CmdScripts Commands Functions

def cmd_connect(args):
    '''Command CONNECT (make a Serial Connection)'''
    global ser
    # Check for expected number of arguments
    if len(args) < 2:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("CONNECT"))
        return False
    # Get and check arguments
    serial_port = args[0]
    serial_bauds = args[1]
    if not is_int(serial_bauds):
        print_log(LOG.ERROR, TEXT.CONNECT_INVALID_BAUDS)
        return False
    serial_bauds = int(serial_bauds)
    # Try to open the serial port
    print_log(LOG.INFO, TEXT.CONNECT_OPENING.format(serial_port, serial_bauds))
    ser = serial_open(serial_port, serial_bauds, res_timeout, 1.0)
    if (ser is None) or (not ser.isOpen()):
        print_log(LOG.INFO, TEXT.CONNECT_OPEN_FAIL)
        return False
    print_log(LOG.INFO, TEXT.CONNECT_OPEN)
    return True


def cmd_disconnect(args):
    '''Command DISCONNECT (make a Serial Connection)'''
    global ser
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("DISCONNECT"))
        return False
    serial_port = args[0]
    # Just close current porresponset (multiple ports support unimplemnted)
    if (ser is not None) and ser.isOpen():
        serial_close(ser)
    print_log(LOG.INFO, TEXT.DISCONNECT_CLOSE)
    return True


def cmd_cfrestimeout(args):
    '''Command CFGRESTIMEOUT (set Serial read timeout)'''
    global res_timeout
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("CFGRESTIMEOUT"))
        return False
    # Check for valid timeout value
    if not is_int(args[0]):
        print_log(LOG.ERROR, TEXT.CFGRESTIMEOUT_INVALID)
        return False
    res_timeout = int(args[0])/1000
    if ser is not None:
        ser.timeout = res_timeout
    print_log(LOG.INFO, TEXT.CFGRESTIMEOUT_SET.format(res_timeout))
    return True


def cmd_cfgeol(args):
    '''Command CFGEOL (set Serial End Of Line character)'''
    global eol
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("CFGEOL"))
        return False
    # Check for valid EOL value
    if args[0] not in ["CR", "LF", "CRLF"]:
        print_log(LOG.ERROR, TEXT.CFGEOL_INVALID)
        return False
    # Set EOL
    if args[0] == "CR":
        eol = EOL.CR
    elif args[0] == "LF":
        eol = EOL.LF
    elif args[0] == "CRLF":
        eol = EOL.CRLF
    print_log(LOG.INFO, TEXT.CFGEOL_SET.format(args[0]))
    return True


def cmd_delay(args):
    '''Command DELAY (wait for some seconds)'''
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("DELAY"))
        return False
    # Check for valid time value
    if not is_int(args[0]):
        print_log(LOG.ERROR, TEXT.DELAY_INVALID)
        return False
    delay_time_s = int(args[0])
    print_log(LOG.INFO, TEXT.DELAY.format(delay_time_s))
    sleep(delay_time_s)
    return True


def cmd_delayms(args):
    '''Command DELAYMS (wait for some milli-seconds)'''
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("DELAYMS"))
        return False
    # Check for valid time value
    if not is_int(args[0]):
        print_log(LOG.ERROR, TEXT.DELAYMS_INVALID)
        return False
    delay_time_ms = int(args[0])
    print_log(LOG.INFO, TEXT.DELAYMS.format(delay_time_ms))
    sleep(delay_time_ms/1000)
    return True


def cmd_eol(args):
    '''Command EOL (send an End Of Line character/s to Serial CLI)'''
    # Send the EOL
    rc = serial_write(ser, eol)
    if rc is None:
        print_log(LOG.ERROR, TEXT.EOL_FAIL)
        return False
    print_log(LOG.INFO, TEXT.EOL_SEND)
    return True


def cmd_command(args):
    '''Command CMD (send a command to Serial CLI)'''
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("CMD"))
        return False
    # Compose command string and add EOL character/s
    cmd_str = " ".join(args)
    cmd_str_eol = "{}{}".format(cmd_str, eol)
    # Send the command
    if not serial_write(ser, cmd_str_eol):
        print_log(LOG.ERROR, TEXT.CMD_SEND_FAIL.format(cmd_str))
        return False
    print_log(LOG.INFO, TEXT.CMD_SEND.format(cmd_str))
    return True


def cmd_response(args):
    '''Command RES (read for a response from Serial CLI)'''
    # Check for expected number of arguments
    if len(args) < 1:
        print_log(LOG.ERROR, TEXT.CMD_NO_ARGS.format("RES"))
        return False
    # Compose response string to expect
    res_str = " ".join(args)
    # Receive and read response
    res = serial_read_until(ser, res_str, timeout=res_timeout)
    if res == "":
        print_log(LOG.ERROR, TEXT.RES_FAIL.format(res_str, res))
        return False
    print_log(LOG.INFO, TEXT.RES_OK.format(res_str))
    return True


###############################################################################
### CmdScripts Parser & Interpreter Functions

def cmd_script_parse(cmdscript):
    '''Parse cmdscript and check for unexpected or usupported keywords.'''
    # DOS to UNIX EOLs
    cmdscript = cmdscript.replace("\r\n", "\n")
    # Split the text in lines
    cmdscript = cmdscript.split("\n")
    # Iterate over each line detecting wich ones would be ignored
    lines_to_rm_index = []
    for i in range(len(cmdscript)-1):
        line = cmdscript[i]
        # Check for empty and comment lines
        if (len(line) == 0) or (line[0] == "#"):
            lines_to_rm_index.append(i)
            continue
        # Check for unsupported/unkown command
        if line.split()[0] not in CONST.CMDSCRIPT_COMMANDS:
            print_log(LOG.WARNING, TEXT.UNEXPECTED_CMDSCRIPT_CMD.format(line))
            lines_to_rm_index.append(i)
            continue
    # Remove lines to ignore from cmdscript
    removed = 0
    for i in lines_to_rm_index:
        del cmdscript[i-removed]
        removed = removed + 1
    return cmdscript


def cmdscript_interpreter(cmdscript):
    '''cmdscript interpreter'''
    for line in cmdscript:
        command = line.split()
        operation = command[0]
        args = command[1:]
        # Ignore unsupported operations
        if operation not in CONST.CMDSCRIPT_COMMANDS:
            continue
        # Handle Commands
        if operation == "CONNECT":
            if not cmd_connect(args):
                return False
        elif operation == "DISCONNECT":
            if not cmd_disconnect(args):
                return False
        elif operation == "CFGRESTIMEOUT":
            if not cmd_cfrestimeout(args):
                return False
        elif operation == "CFGEOL":
            if not cmd_cfgeol(args):
                return False
        elif operation == "DELAY":
            if not cmd_delay(args):
                return False
        elif operation == "DELAYMS":
            if not cmd_delayms(args):
                return False
        elif operation == "EOL":
            if not cmd_eol(args):
                return False
        elif operation == "CMD":
            if not cmd_command(args):
                return False
        elif operation == "RES":
            if not cmd_response(args):
                return False
        else:
            print_log(LOG.WARNING, TEXT.INVALID_CMDSCRIPT_CMD.format(command))
    return True

###############################################################################
### Main Function

def main(argc, argv):
    '''Main Function.'''
    # Check and parse program options from arguments
    #options = parse_options()
    ## Input cmdscript file to use
    #if options["file"] is None:
    #    show_help()
    #    sys_exit(RC.OK)
    #filepath_cmdscript = options["file"][0]
    filepath_cmdscript = CONST.SCRIPT_PATH + "/cmdscript.txt"
    # Read, parse and check if cmdscript is valid
    cmdscript = file_read_all_text(filepath_cmdscript)
    cmdscript = cmd_script_parse(cmdscript)
    # Launch cmdscript interpreter
    rc = cmdscript_interpreter(cmdscript)
    # Program end
    if not rc:
        program_exit(RC.FAIL)
    program_exit(RC.OK)

###############################################################################
### Exit Function

def program_exit(return_code):
    '''Finish function.'''
    global ser
    # Check if unexpected exit code provided and use RC.FAIL in that case
    if (return_code != RC.OK) and (return_code != RC.FAIL):
        return_code = RC.FAIL
    # Close and free any pending memory
    if (ser is not None) and ser.isOpen():
        serial_close(ser)
    # Exit
    print_log(LOG.DEBUG, "Program exit ({}).\n".format(return_code))
    sys_exit(return_code)

###############################################################################
### Main Script execution Check

if __name__ == "__main__":
    try:
        main(len(sys_argv), sys_argv)
    except KeyboardInterrupt:
        g_terminal_close = True
        th_read.join()
        th_write.join()
        program_exit(RC.OK)
