# -*- coding: utf-8 -*-
import os
import sys


def userinput():
    newconf = []
    newconf.append(input("Benutzername: "))  # 0
    newconf.append(input("Benutzertoken: "))  # 1
    newconf.append(input("Logfile: "))  # 2
    newconf.append(input("Device-ID: "))  # 3
    newconf.append(input("Device Name: "))  # 4
    newconf.append(input("Device Typ: "))  # 5
    newconf.append(input("Device Gruppe: "))  # 6
    newconf.append(input("Device Hauptgruppe: "))  # 7
    newconf.append(input("JSON Inputdatei: "))  # 8
    newconf.append(input("Sensorlogger URL: "))  # 9
    newconf.append(input("Temperatursensor ID: "))  # 10
    newconf.append(input("Luftfeuchtigkeitssensor ID: "))  # 11
    newconf.append(input("Wieviele Sensoren sind vorhanden?: "))  # 12
    return newconf


def sensordata(var):
    sensor = [[] for i in range(int(var))]
    sensor.append(var)
    for i in range(0, int(var)):
        sensor[i].append(i)
        sensor[i].append(input("Name von Sensor " + (str(int(i) + 1)) + ": "))
        sensor[i].append(input("Messwert Sensor " + (str(int(i) + 1)) + ": "))
        sensor[i].append(input("Einheit von Sensor " + (str(int(i) + 1)) + ": "))
    return sensor

def createconf(configfile):
    if os.path.isfile(configfile):
        print("[Fehler] Konfigurationsdatei [%s] bereits vorhanden. Bitte gebe mit [-c neue.config] eine neue Konfigurationsdatei an." % configfile)
        sys.exit(1)
    else:
        data = userinput()
        sensor = sensordata(int(data[12]))

        sensorlines = []
        sensorlines.append('')
        sensorlines.append('[SENSOREN]')
        sensorlines.append('anzahl = ' + str(data[12]))
        sensorlines.append('')
        for i in range(0, int(data[12])):
            sensorlines.append('[SENSOR' + str(sensor[i][0]+1) + ']')
            sensorlines.append('sensorname' + str(sensor[i][0]+1) + ' = ' + str(sensor[i][1]))
            sensorlines.append('sensorwert' + str(sensor[i][0]+1) + ' = ' + str(sensor[i][2]))
            sensorlines.append('sensoreinheit' + str(sensor[i][0]+1) + ' = ' + str(sensor[i][3]))
            sensorlines.append('')

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
            'deviceName = ' + str(data[4]),
            'deviceTyp = ' + str(data[5]),
            'deviceGroup = ' + str(data[6]),
            'deviceMainGrp = ' + str(data[7]),
            'tempID = ' + str(data[10]),
            'HumidityID = ' + str(data[11]),
            '',
            '[DATA]',
            'input = ' + str(data[8]),
            'logurl = ' + str(data[9]),
            'removejson = False',
            ''
            ]
        try:
            with open(configfile, mode="w", encoding="utf-8") as config:
                config.write('\n'.join(conflines))
            with open(configfile, mode="a", encoding="utf-8") as config:
                config.write('\n'.join(sensorlines))
            print("[OK] Konfigurationsdatei [%s] erstellt." % configfile)
            sys.exit(0)
        except IOError as e:
            print(("[Fehler] Konfigurationsdatei [%s] konnte nicht geschrieben werden. [%s]" % (configfile, e.strerror)))
            sys.exit(1)
