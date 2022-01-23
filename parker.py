#!/usr/bin/env python3

# POTA Field Logger, "Parker"
# Copyright 2022 Mike Case, W8MSC

# Basic field logging program
# Takes the required minimum fields for a QSO and logs them to an ADIF


try:
    import logging
    import datetime
    from tkinter import *
    from tkinter import messagebox
    import os
    #import sqlite3
except ImportError:
    print("You are not using Python 3")
    exit()

validBands = ["1.25CM", "70CM", "2M", "4M",
              "6M", "10M", "12M", "15M", "17M",
              "20M", "30M", "40M", "60M", "80M", "160M"
              ]

validModes = [
    "CW", "FM", "SSB"
]

validYears = [2016, 2017, 2018, 2019, 2020, 2021, 2022]

validMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

validDays = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
             16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

validHours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

validMinutes = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
]

validSeconds = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
]

validCallsignCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/"
validReferenceCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,"

APPTITLE = "POTA Field Logger"
# WINDOWSIZE="700x350"

# Globals
info = {}
info['programversion'] = '0.2.18'
info['programid'] = "POTA Field Logger"
info['copyrightYear'] = '2022'
logbook = []

# Store the Station callsign, park, and date of the first QSO
STATION = ""
PARK = ""
STARTDATE = ""  # get this from the first qso-- duh
STARTDATETIME = ""

# start logging
logging.basicConfig(filename='parker.log', level=logging.DEBUG)
logging.debug("Begin DEBUG logging")


def aboutMsg():
    """ Display an About message box """

    displayMsg = "{} version {}\n\nCopyright {}, W8MSC\n\nParks On The Air\nwww.parksontheair.com".format(
        info['programid'],
        info['programversion'],
        info['copyrightYear']
    )
    messagebox.showinfo('About', displayMsg)


def addentry(event=None):
    """ Add valid QSOs to the logbook """

    # Use the entry widget to also process control commands
    # parse the incoming string and switch band/mode if matches valid lists

    cmd = callStr.get().upper()
    if cmd in validBands:
        setBand(cmd)
        print(datetimeString() + " Setting mode to " + cmd)
        resetCall()
        return

    if cmd in validModes:
        setMode(cmd)
        print(datetimeString() + " Setting mode to " + cmd)
        resetCall()
        return

    global STATION, PARK, STARTDATE
    updateDateTime()

    qso = {}
    qso["station_callsign"] = stationStr.get().upper()
    if operatorStr.get():
        qso["operator"] = operatorStr.get().upper()
    qso["qso_date"] = ("{:04}{:02}{:02}".format(
        yearInt.get(), monthInt.get(), dayInt.get()))
    qso["time_on"] = ("{:02}{:02}{:02}".format(
        hourInt.get(), minuteInt.get(), secondInt.get()))
    qso["call"] = callStr.get().upper()
    qso["band"] = bandStr.get()
    qso["mode"] = modeStr.get()
    qso["my_sig"] = "POTA"
    qso["my_sig_info"] = parkStr.get().upper()
    qso["comment"] = commentStr.get()

    if p2pStr.get():
        qso["sig"] = "POTA"
        # this does not validate the other station's reference
        qso["sig_info"] = p2pStr.get().upper()
    else:
        pass

    # Set global variables with the first QSO info
    if len(logbook) == 0:
        STATION = qso["station_callsign"]
        PARK = qso["my_sig_info"]
        STARTDATE = qso["qso_date"]

    if checkRequiredFields():
        qsotext = (datetimeString() +
                   "QSO by station {} ".format(qso["station_callsign"]))
        if "operator" in qso:
            qsotext + ("operator {}".format(qso["operator"]))
        qsotext + (" on date {} at time {} at park {} with {} ".format(
            qso["qso_date"],
            qso["time_on"],
            qso["my_sig_info"],
            qso["call"],
        ))
        if "sig_info" in qso:
            qsotext + ("their park {} ".format(qso["sig_info"]))
        qsotext + (" on band {} using mode {} comment {}".format(
            qso["band"],
            qso["mode"],
            qso["comment"]
        ))
        print(qsotext)
        logbook.append(qso)
        logging.info(qsotext)
        print(qso)
        resetP2P()
        resetComment()
        resetCall()
        lockStation()
        lockPark()
        updateStatusBar()
        cE.focus_set()
    else:
        print("Nothing to enter")


def bandcallback(selection):
    """ Updates the BAND when the selection is changed """

    bandStr.set(selection)


def checkRequiredFields():
    """ Checks that all the required fields for a QSO are set """
    # This will update some GUI controls for visual feedback when not set

    goodtogo = TRUE

    # make sure station callsign field has something in it
    x = stE.get()
    if len(x) > 0:
        stE.config(bg='white')
    else:
        stE.config(bg='red')
        goodtogo = FALSE

    # make sure park field has something in it
    x = pE.get()
    if len(x) > 0:
        pE.config(bg='white')
    else:
        pE.config(bg='red')
        goodtogo = FALSE

    # make sure call sign being worked field has something in it
    x = cE.get()
    if len(x) > 0:
        cE.config(bg='white')
    else:
        cE.config(bg='red')
        goodtogo = FALSE

    # make sure band field has something in it
    x = bandStr.get()
    if len(x) > 0:
        bL.config(bg=defBG)
    else:
        bL.config(bg="red")
        goodtogo = FALSE

    # make sure mode field has something in it
    x = modeStr.get()
    if len(x) > 0:
        mL.config(bg=defBG)
    else:
        mL.config(bg="red")
        goodtogo = FALSE

    if goodtogo:
        return TRUE
    else:
        return FALSE


def clicked():
    """ Test function for bindings """

    global unsaved
    unsaved = 1
    print("Inside function clicked")


def createDatabase():
    """ Create the database if not exists """

    print("Entered createDatabase")


def datetimeString():
    now = datetime.datetime.utcnow()
    return("{:04}{:02}{:02}-{:02}{:02}{:02}: ".format(now.year, now.month, now.day, now.hour, now.minute, now.second))


def displayHelpMsg():
    """ Display an About message box """

    displayMsg = """
        Keys:\n
    Control-h  Increments the hour
    Control-H  Decrements the hour
    Control-m  Increments the minute
    Control-M  Decrements the minute
    Control-s  Increments the second
    Control-S  Decrements the second
    Control-c  Focus on the callsign
    Control-p  Focus on their park
    ESC  Wipes incomplete QSO
    ENTER  Saves the current QSO
    """

    helpWin = Frame()
    messagebox.showinfo('About', displayMsg)


def displayTime():
    """ update the UTC and local time displays """

    now = datetime.datetime.utcnow()
    local = datetime.datetime.now()

    if liveLogging.get() is True:
        yearInt.set(now.year)
        monthInt.set(now.month)
        dayInt.set(now.day)
        hourInt.set(now.hour)
        minuteInt.set(now.minute)
        secondInt.set(now.second)

    nowUTC = ("{:04}/{:02}/{:02} {:02}:{:02}:{:02}".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    ))

    app.after(1000, displayTime)


def focusCallsign(self):
    """ Set the focus to the other station's callsign textbox when shortcut is invoked """
    cE.focus_set()


def focusPark(self):
    """ Set the focus to the other stations's park textbox when shortcut is invoked """
    p2pE.focus_set()


def goodbye():
    """ Quits the program and preforms housekeeping to write the logbook to a file """

    print("There are {} QSOs in the logbook".format(len(logbook)))
    writeADIF()
    print("Goodbye")
    app.destroy()


def loggingModeCallback():
    """ Update the vars for date and time """

    if liveLogging.get() is True:
        # disable the date and time entries
        yearE.configure(state='disabled')
        monthE.configure(state='disabled')
        dayE.configure(state='disabled')
        hourE.configure(state='disabled')
        minuteE.configure(state='disabled')
        secondE.configure(state='disabled')

    else:
        # enable the date and time entries
        yearE.configure(state='normal')
        monthE.configure(state='normal')
        dayE.configure(state='normal')
        hourE.configure(state='normal')
        minuteE.configure(state='normal')
        secondE.configure(state='normal')


def lockPark():
    """ Once the first QSO is recorded lock the park to prevent changes """

    pE.config(state='disabled')


def lockStation():
    """ Once the first QSO is recorded lock the station callsign """

    stE.config(state='disabled')


def modecallback(selection):
    """ Updates the MODE when the pulldown is changed """

    modeStr.set(selection)


def qsoToStr(qso):
    """ Convert a QSO dictionary to string """
    # switch if the optional p2p info is available

    str = ""  # start with new string
    if "station_callsign" in qso:
        str += ("<STATION_CALLSIGN:{}>{} ".format(
            len(qso["station_callsign"]), qso["station_callsign"]))
    if "operator" in qso:
        str += ("<OPERATOR:{}>{} ".format(
            len(qso["operator"]), qso["operator"]))
    if "call" in qso:
        str += ("<CALL:{}>{} ".format(
            len(qso["call"]), qso["call"]))
    if "qso_date" in qso:
        str += ("<QSO_DATE:{}>{} ".format(
            len(qso["qso_date"]), qso["qso_date"]))
    if "time_on" in qso:
        str += ("<TIME_ON:{}>{} ".format(
            len(qso["time_on"]), qso["time_on"]))
    if "band" in qso:
        str += ("<BAND:{}>{} ".format(
            len(qso["band"]), qso["band"]))
    if "mode" in qso:
        str += ("<MODE:{}>{} ".format(
            len(qso["mode"]), qso["mode"]))
    if "my_sig" in qso:
        str += ("<MY_SIG:{}>{} ".format(
            len(qso["my_sig"]), qso["my_sig"]))
    if "my_sig_info" in qso:
        str += ("<MY_SIG_INFO:{}>{} ".format(
            len(qso["my_sig_info"]), qso["my_sig_info"]))
    if "sig" in qso:
        str += ("<SIG:{}>{} ".format(
            len(qso["sig"]), qso["sig"]))
    if "sig_info" in qso:
        str += ("<SIG_INFO:{}>{} ".format(
            len(qso["sig_info"]), qso["sig_info"]))
    str += "<EOR>"
    return str


"""     if "sig_info" in qso:   # this one is for P2P qsos
        str = ("<STATION_CALLSIGN:{}>{} ".format(len(qso["station_callsign"]), qso["station_callsign"]) +
               "<OPERATOR:{}>{} ".format(len(qso["operator"]), qso["operator"]) +
               "<CALL:{}>{} ".format(len(qso["call"]), qso["call"]) +
               "<QSO_DATE:{}>{} ".format(len(qso["qso_date"]), qso["qso_date"]) +
               "<TIME_ON:{}>{} ".format(len(qso["time_on"]), qso["time_on"]) +
               "<BAND:{}>{} ".format(len(qso["band"]), qso["band"]) +
               "<MODE:{}>{} ".format(len(qso["mode"]), qso["mode"]) +
               "<MY_SIG:{}>{} ".format(len(qso["my_sig"]), qso["my_sig"]) +
               "<MY_SIG_INFO:{}>{} ".format(len(qso["my_sig_info"]), qso["my_sig_info"]) +
               "<SIG:{}>{} ".format(len(qso["sig"]), qso["sig"]) +
               "<SIG_INFO:{}>{} ".format(len(qso["sig_info"]), qso["sig_info"]) +
               "<EOR>")
    else:   # this one if for non-P2P qsos
        str = ("<STATION_CALLSIGN:{}>{} ".format(len(qso["station_callsign"]), qso["station_callsign"]) +
               "<OPERATOR:{}>{} ".format(len(qso["operator"]), qso["operator"]) +
               "<CALL:{}>{} ".format(len(qso["call"]), qso["call"]) +
               "<QSO_DATE:{}>{} ".format(len(qso["qso_date"]), qso["qso_date"]) +
               "<TIME_ON:{}>{} ".format(len(qso["time_on"]), qso["time_on"]) +
               "<BAND:{}>{} ".format(len(qso["band"]), qso["band"]) +
               "<MODE:{}>{} ".format(len(qso["mode"]), qso["mode"]) +
               "<MY_SIG:{}>{} ".format(len(qso["my_sig"]), qso["my_sig"]) +
               "<MY_SIG_INFO:{}>{} ".format(len(qso["my_sig_info"]), qso["my_sig_info"]) +
               "<EOR>") """
# return str


def resetCall():
    """ Clear the worked callsign textbox once the QSO is logged """

    cE.delete(0, END)


def resetP2P():
    """ Clear the other station's park once the QSO is logged """

    p2pE.delete(0, END)


def resetComment():
    """ Clear the comment field once the QSO is logged """

    comE.delete(0, END)


def setBand(band):
    bandStr.set(band)


def setMode(mode):
    modeStr.set(mode)


def updateDateTime():
    """ Update the date and time fields when the QSO gets added """

    now = datetime.datetime.utcnow()
    qso_date = ("%04d%02d%02d" % (now.year, now.month, now.day))
    time_on = ("%02d%02d%02d" % (now.hour, now.minute, now.second))

    qsodateStr.set(qso_date)
    qsotimeStr.set(time_on)


def updateStatusBar():
    """ Update the status bar with the total QSOs in the logbook """

    #str="There are {} QSOs logged".format(len(logbook))
    # show callsign of last station logged

    str = "Last station logged: {}   -   There are {} QSOs logged".format(
        logbook[-1]["call"],
        len(logbook)
    )
    statusbar.config(text=str)


def callbackStationCallsign(*args):
    """ Convert whatever is in station callsign to upper case and enforce only valid characters """
    temp = ""
    for char in stationStr.get().upper():
        if char in validCallsignCharacters:
            temp += char
    stationStr.set(temp)


def callbackOperatorCallsign(*args):
    """ Convert whatever is in operator callsign to upper case and enforce only valid characters """
    temp = ""
    for char in operatorStr.get().upper():
        if char in validCallsignCharacters:
            temp += char
    operatorStr.set(temp)


def callbackHunterCallsign(*args):
    """ Convert whatever is in hunter callsign to upper case and enforce only valid characters """
    temp = ""
    for char in callStr.get().upper():
        if char in validCallsignCharacters:
            temp += char
    callStr.set(temp)


def callbackMyPark(*args):
    """ Convert whatever is in my park to upper case and enforce only valid characters """
    temp = ""
    for char in parkStr.get().upper():
        if char in validReferenceCharacters:
            temp += char
    parkStr.set(temp)


def callbackTheirPark(*args):
    """ Convert whatever is in their park to upper case and enforce only valid characters """
    temp = ""
    for char in p2pStr.get().upper():
        if char in validReferenceCharacters:
            temp += char
    p2pStr.set(temp)


def warningMsg():
    """ Display an About message box """

    displayMsg = """Parker is ALPHA quality software!
    \n
DO NOT USE THIS PROGRAM FOR REAL QSO LOGGING UNLESS YOU HAVE AN ALTERNATE LOGGING METHOD AVAILABLE!!"""
    messagebox.showinfo('Warning!', displayMsg, icon='warning')


def wipeQSO(event):
    """ Erase an unfinished QSO """

    resetCall()
    resetComment()
    resetP2P()


def writeADIF():
    """ Writes the logbook to a ADI file """

    # file naming convention
    # STATION_CALLSIGN@REFERENCE_YYYYMMDD-HHMMSS.adif
    # w8msc@K-1234_20191201-123456.adi

    # TODO doublecheck target doesn't already exist and

    now = datetime.datetime.utcnow()
    nowDate = ("%04d%02d%02d" % (now.year, now.month, now.day))
    nowTime = ("%02d%02d%02d" % (now.hour, now.minute, now.second))

    global info
    global STARTDATETIME

    if len(logbook) > 0:
        # set date and time portion of filename to first qso
        STARTDATETIME = "{}-{}".format(logbook[0]
                                       ['qso_date'], logbook[0]['time_on'])
        #print("Start Date/Time = " + STARTDATETIME)

        outputfile = ("{}@{}_{}.adif".format(STATION, PARK, STARTDATETIME))

        # modify callsigns with slash to dash to prevent OS filepath problems
        outputfile = outputfile.replace("/", "-")

        print("outfile = " + outputfile)
        # TODO check if the output file already exists
        outfile = open(outputfile, 'w')

        # write ADIF header from globals
        outfile.write("Parks On The Air Field Logger\n")
        outfile.write("PROGRAMID:{}>{}\n".format(
            len(info['programid']), info['programid']))
        outfile.write("PROGRAMVERSION:{}>{}\n".format(
            len(info['programversion']), info['programversion']))
        outfile.write("CREATED_TIMESTAMP:13>{} {}".format(nowDate, nowTime))

        # insert metadata headers for :
        #   rig, power, antenna, comments, county

        outfile.write("<EOH>\n")
        for qso in logbook:
            outfile.write(qsoToStr(qso)+'\n')
        outfile.close()
    else:
        print("No QSOs in logged, skipping creation of the ADIF log file")


def incDay(event):
    """ increments the Day, wrap around at 31 """

    if dayInt.get() == 31:
        dayInt.set(00)
    else:
        now = dayInt.get()
        now += 1
        dayInt.set(now)
    displayTime()


def decDay(event):
    """ decrements the day, wrap around at 0 """

    if dayInt.get() == 0:
        dayInt.set(31)
    else:
        now = dayInt.get()
        now -= 1
        dayInt.set(now)
    displayTime()


def incHour(event):
    """ increments the hour, wrap around at 23 """

    if hourInt.get() == 23:
        hourInt.set(00)
    else:
        now = hourInt.get()
        now += 1
        hourInt.set(now)
    displayTime()


def decHour(event):
    """ decrements the hour, wrap around at 0 """

    if hourInt.get() == 0:
        hourInt.set(23)
    else:
        now = hourInt.get()
        now -= 1
        hourInt.set(now)
    displayTime()


def incMinute(event):
    """ increments the minute, wrap around at 59 """

    if minuteInt.get() == 59:
        minuteInt.set(00)
    else:
        now = minuteInt.get()
        now += 1
        minuteInt.set(now)
    displayTime()


def decMinute(event):
    """ decrements the minute, wrap around at 0 """

    if minuteInt.get() == 0:
        minuteInt.set(59)
    else:
        now = minuteInt.get()
        now -= 1
        minuteInt.set(now)
    displayTime()


def incSecond(event):
    """ increments the second, wrap around at 59 """

    if secondInt.get() == 59:
        secondInt.set(00)
    else:
        now = secondInt.get()
        now += 1
        secondInt.set(now)
    displayTime()


def decSecond(event):
    """ decrements the second, wrap around at 00 """

    if secondInt.get() == 0:
        secondInt.set(59)
    else:
        now = secondInt.get()
        now -= 1
        secondInt.set(now)
    displayTime()


# create the GUI
app = Tk()
#app.master.title("POTA Field Logger")

# qsoframe=LabelFrame(app,text="QSO Details",padx=5,pady=5)
# qsoframe.pack(fill="both", expand="yes",padx=5,pady=5)

# assign types for the various inputs
defBG = app.cget("background")
stationStr = StringVar()
operatorStr = StringVar()
parkStr = StringVar()
callStr = StringVar()
yearStr = StringVar()
monthStr = StringVar()
dayStr = StringVar()
dateStr = StringVar()
bandStr = StringVar()
modeStr = StringVar()
commentStr = StringVar()
p2pStr = StringVar()
qsodateStr = StringVar()
qsotimeStr = StringVar()
timeStr = StringVar()
theirParkStr = StringVar()
yearInt = IntVar()
monthInt = IntVar()
dayInt = IntVar()
hourInt = IntVar()
minuteInt = IntVar()
secondInt = IntVar()
liveLogging = BooleanVar()
liveLogging.set(True)

app.title(APPTITLE)
# app.geometry(WINDOWSIZE)

# create the menubar
menu = Menu(app)
fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label="Open", command=clicked)
fileMenu.add_command(label="Exit", command=goodbye)
helpMenu = Menu(menu, tearoff=0)
helpMenu.add_command(label="Help", command=displayHelpMsg)
helpMenu.add_command(label="About", command=aboutMsg)
menu.add_cascade(label="File", menu=fileMenu)
menu.add_cascade(label="Help", menu=helpMenu)
app.config(menu=menu)

stL = Label(app, text="My Station Call").grid(row=0, column=0)
stE = Entry(app, textvariable=stationStr)
stE.grid(row=1, column=0)
stationStr.trace('w', callbackStationCallsign)

opL = Label(app, text="Operator").grid(row=0, column=1)
opE = Entry(app, textvariable=operatorStr)
opE.grid(row=1, column=1)
operatorStr.trace('w', callbackOperatorCallsign)

pL = Label(app, text="My Park").grid(row=0, column=2)
pE = Entry(app, textvariable=parkStr)
pE.grid(row=1, column=2)
parkStr.trace('w', callbackMyPark)

yearL = Label(app, text="Year").grid(row=0, column=3)
yearE = Entry(app, width=4, textvariable=yearInt, state='disabled')
yearE.grid(row=1, column=3, sticky="ew")

monthL = Label(app, text="Month").grid(row=0, column=4)
monthE = Entry(app, textvariable=monthInt, width=2, state='disabled')
monthE.grid(row=1, column=4, sticky="ew")

dayL = Label(app, text="Day").grid(row=0, column=5)
# dayE=Entry(app,textvariable=dayInt,width=2,state='disabled')
dayE = Spinbox(app, textvariable=dayInt, from_=0,
               to=31, width=2, state='disabled')
dayE.grid(row=1, column=5, sticky="ew")

hourL = Label(app, text="Hour").grid(row=0, column=6)
hourE = Spinbox(app, textvariable=hourInt, from_=0,
                to=23, width=2, state='disabled')
hourE.grid(row=1, column=6, sticky="ew")

minuteL = Label(app, text="Minute").grid(row=0, column=7)
minuteE = Spinbox(app, textvariable=minuteInt, from_=0,
                  to=59, width=2, state='disabled')
minuteE.grid(row=1, column=7, sticky="ew")

secondL = Label(app, text="Second").grid(row=0, column=8)
secondE = Spinbox(app, textvariable=secondInt, width=2,
                  from_=0, to=59, state='disabled')
secondE.grid(row=1, column=8, sticky="ew")

# the station being worked
cL = Label(app, text="Call").grid(row=2, column=0)
cE = Entry(app, textvariable=callStr)
cE.grid(row=3, column=0)
callStr.trace('w', callbackHunterCallsign)

# the mode and band being used
bL = Label(app, text='Band')
bL.grid(row=0, column=9)
bands = OptionMenu(app, bandStr, *validBands, command=bandcallback)
bands.grid(row=1, column=9)

mL = Label(app, text='Mode')
mL.grid(row=0, column=10)
modes = OptionMenu(app, modeStr, *validModes, command=modecallback)
modes.grid(row=1, column=10)

p2pL = Label(app, text="Their Park")
p2pL.grid(row=2, column=1)
p2pE = Entry(app, textvariable=p2pStr)
p2pE.grid(row=3, column=1)
p2pStr.trace('w', callbackTheirPark)

comL = Label(app, text="Comment")
comL.grid(row=2, column=2)
comE = Entry(app, textvariable=commentStr)
comE.grid(row=3, column=2, columnspan=4, sticky="ew")

bAdd = Button(app, text="Add QSO", command=addentry).grid(row=3, column=9)
bQuit = Button(app, text="Quit", command=goodbye).grid(row=3, column=10)

modeL = Label(app, text="Time Entry Mode").grid(row=2, column=6, columnspan=2)
r1 = Radiobutton(app, text="Live", variable=liveLogging,
                 value=True, command=loggingModeCallback)
r1.grid(row=3, column=6)
r2 = Radiobutton(app, text="Manual", variable=liveLogging,
                 value=False, command=loggingModeCallback)
r2.grid(row=3, column=7)

blankRow = Label(app, text=" ")
blankRow.grid(row=6, column=0)

statusbar = Label(app, text="POTA Field Logger is ALPHA quality - Not ready for real use",
                  bd=1, relief=SUNKEN, anchor=W)
statusbar.grid(row=7, column=0, columnspan=11, sticky="ew")

# Add some key bindings
app.bind('<Return>', addentry)
app.bind('<KP_Enter>', addentry)
app.bind('<Escape>', wipeQSO)
app.bind("<Control-Key-d>", incDay)
app.bind("<Control-Key-D>", decDay)
app.bind("<Control-Key-h>", incHour)
app.bind("<Control-Key-H>", decHour)
app.bind("<Control-Key-m>", incMinute)
app.bind("<Control-Key-M>", decMinute)
app.bind("<Control-Key-s>", incSecond)
app.bind("<Control-Key-S>", decSecond)
app.bind("<Control-Key-c>", focusCallsign)
app.bind("<Control-Key-p>", focusPark)

warningMsg()
displayTime()

app.mainloop()
