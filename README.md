# Parker
## Parks On The Air field logging program

Parker is a simple logging program to record QSOs for the Parks On The Air (POTA) program.

It is designed to be a simple log entry program to record the required information for park contacts.  It does not require internet access to log contacts, but some additional features may need occasional access to update internal files.

## Limitations

* Parker is in alpha testing.  You should have alternate logging methods available to you if you encounter any problems with Parker.
* It is not designed to be a log database or QSL service.
* No rig control is provided or planned.
* It does not provide separate fields for optional exchange information, such as hunter's name, QTH, RSTs, or contest exchange.
* Callsigns and park fields are not checked for proper format.  Garbage in, garbage out.


## Installation

Parker is written in Python3 and Tkinter for cross-platform support.  

Unzip the Parker archive to a folder on your computer.

The parker executable does not need to be in your PATH.  The python libraries do need to be available, however.

The Linux Mint default install is missing some packages.

Install the missing packages:

```
sudo apt update
sudo apt upgrade
sudo apt install python3-tkinter python3-websocket
```

Set Linux Mint to use python3 by default

```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

For Linux you can make parker.py executable with

chmod +x parker.py

## Running

Start the program, either from a desktop shortcut or by command line.  
* Tip:  You can see addtional information by running via command line. 
* Bonus tip:  Parker.log contains a history of log events.

## Required fields:

* My Station Callsign:  Enter the callsign you give out over the air.
* My Park:  Enter the park reference with the dash between program code and numeric portion.
* Date:  Enter the year, month and day.  Parker will format the entries as YYYYMMDD per ADIF standard date.
* Time:  Enter the hour, minute, second.  Parker will format the entries as HHMMSS per ADIF standard time.
* Band:  Select from the available list.
* Mode:  Select from the available list.
* Call:  Enter the callsign of the hunter.

## Optional Fields

* Their Park:  Enter the park reference of the hunter if they are in a POTA park.
* Comments:  Enter any supplemental information here such as name, QTH, RSTs, contest exchange info.

# Navigating the interface
## Select the Date/Time logging mode

When Parker is first started it will be in "Live" logging mode.  This allows Parker to use the computer clock to record date and time for QSO entries.  Make sure your computer clock is correct!

Live Logging uses the computer's clock to stamp each QSO with the current time.

Manual Logging requires you to adjust the date and time manually for each QSO.  Use this mode for transcription of paper logs.

Once the first QSO is made the My Call and My Park fields will lock to prevent accidental changes to these fields.

## Keyboard shortcuts

Keyboard shortcuts can reduce the need to use a mouse for logging.

* TAB moves forward between fields
* Shift-TAB moves backwards between fields
* ENTER to save QSO

Hot-keys:
* Control-d increments the date
* Control-D decrements the date
* Control-h increments the hour
* Control-H decrements the hour
* Control-m increments the minute
* Control-M decrements the minute
* Control-c focus on the call entry
* Control-p focus on their park entry
* ESC to erase/wipe an incomplete entry

# Saving your log files

## Filename format
Parker will automatically name your exported file.
It will be in a format that allows easy recognition of your callsign, park, date and time of your activation (FUTURE: and POTA location code)

CALLSIGN@REFERENCE-YYYYMMDD_HHMMSS.adi

The timestamp of the first QSO logged is used for the timestamp of the file.

The files are located in the working directory where Parker was started from.

## Best Practices
Parker generates standard ADIF log files.  
If you use a QSO database program you can import the activation log generated by Parker into your preferred logging program.

Store copies of your log files on cloud storage drive such as Dropbox, iCloud, OneDrive



## Comments, Suggestions

Send feedback to w8msc@parksontheair.com
