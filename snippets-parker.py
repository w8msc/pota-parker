# python snippet for string builder
        qsotext = datetimeString()
        qsotext += ("QSO by station {} ".format(qso["station_callsign"]))
        if "operator" in qso:
            qsotext += ("operator {} ".format(qso["operator"]))
        qsotext += ("on date {} ".format(qso["qso_date"]))
        qsotext += ("at time {} ".format(qso["time_on"]))
        qsotext += ("at park {} ".format(qso["my_sig_info"]))
        qsotext += ("with {} ".format(qso["call"]))
        qsotext += ("on band {}".format(qso["band"]))
        qsotext += ("using mode {} ".format(qso["mode"]))
        qsotext += ("comment {}".format(qso["comment"]))



        qsotext = (datetimeString() + "QSO by station {} operator {} on date {} at time {} at park {} with {} on band {} using mode {} comment {}".format(
                qso["station_callsign"],
                qso["operator"],
                qso["qso_date"],
                qso["time_on"],
                qso["my_sig_info"],
                qso["call"],
                qso["band"],
                qso["mode"],
                qso["comment"]
            ))


            qsotext = (datetimeString() + "QSO by station {} operator {} on date {} at time {} at park {} with {} on band {} using mode {} their park {} comment {}".format(
                stationStr.get().upper(),
                operatorStr.get().upper(),
                qsodateStr.get(),
                qsotimeStr.get(),
                parkStr.get().upper(),
                callStr.get().upper(),
                bandStr.get(),
                modeStr.get(),
                p2pStr.get().upper(),
                commentStr.get())
            )