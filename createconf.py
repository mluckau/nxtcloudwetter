# -*- coding: utf-8 -*-
import os
import sys


def userinput():
    newconf = []
    newconf.append(input("Benutzername: "))  # 0
    newconf.append(input("Benutzertoken: "))  # 1
    newconf.append(input("Logfile: "))  # 2
    newconf.append(input("Device-ID: "))  # 3
    newconf.append(input("JSON Inputdatei: "))  # 4
    newconf.append(input("Sensorlogger URL: "))  # 5
    newconf.append(input("Temperatursensor ID: "))  # 6
    newconf.append(input("Luftfeuchtigkeitssensor ID: "))  # 7
    return newconf


def createconf(configfile):
    if os.path.isfile(configfile):
        print("[Fehler] Konfigurationsdatei [%s] bereits vorhanden. Bitte gebe mit [-c neue.config] eine neue Konfigurationsdatei an." % configfile)
        sys.exit(1)
    else:
        data = userinput()
        conflines = [
                '[USER]',
                'username = ' + str(data[0]),
                'token = ' + str(data[1]),
                '',
                '[LOG]',
                'file = ' + str(data[2]),
                '',
                '[DEVICE]',
                'deviceId = ' + str(data[3]),
                'tempID = ' + str(data[6]),
                'HumidityID = ' + str(data[7]),
                '',
                '[DATA]',
                'input = ' + str(data[4]),
                'logurl = ' + str(data[5]),
                'removejson = False'
            ]
        try:
            with open(configfile, 'w') as config:
                config.write('\n'.join(conflines))
            print("[OK] Konfigurationsdatei [%s] erstellt. Bitte passe sie an deine Umgebung an." % configfile)
            sys.exit(0)
        except IOError as e:
            print(("[Fehler] Konfigurationsdatei [%s] konnte nicht geschrieben werden. [%s]" % (configfile, e.strerror)))
            sys.exit(1)
