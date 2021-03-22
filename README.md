# pysercmdscripts

Python tool to automate send commands to a serial command line interface from a *cmdscript* text file that specify commands-responses with a simple language.

Note: Work In Progress, the code was not tested neither validated yet.

## Usage

```bash
python3 pysercmdscripts.py mycmdscript.txt
```

## cmdscript

A **cmdscript** is a plain text file tat uses a special language to specify write-read interactions with a command line interface (CLI), similar to PPP ChatScripts and DuckyScripts.

The cmdscript uses special keywords to specify each operation, here is a list of supported commands:

```text
CONNECT X Y - Open Serial Port "X" at "Y" baudrate speed.
DISCONNECT X - Close Serial Port "X".

CFGEOL X - Configure End Of Line character/s (X: CR, LF, CRLF).
CFGRESTIMEOUT X - Configure RES command response receive tiemout (milli-seconds).

DELAY X - Wait for X seconds.
DELAYMS X - Wait for X milli-seconds.

CMD X Y Z ... - Send the command composed by "X Y Z ...".
RES X Y Z ... - Wait for command response "X Y Z ...".
EOL - Send End Of Line character/s.
```

A simple example of a cmdscript will be the following:

```text
# This line is a comment and will be ignored

# Use Carriage Return character ('\r') as End Of Line character
CFGEOL CR

# Timeout at 300ms if no command response received with RES
CFGRESTIMEOUT 300

# Open Serial Port /dev/ttyUSB0 at 115200 bauds
CONNECT /dev/ttyUSB0 115200

# Send "reboot" command and wait for 10s
CMD reboot
DELAY 10

# Send an End Of Line character/s (enter) and expect to receive "#" as response
EOL
RES #

# Close the Serial Port
DISCONNECT /dev/ttyUSB0
```
