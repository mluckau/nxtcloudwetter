# -*- coding: utf-8 -*-
import os
import sys


def userinput():
    conf = {}
    conf['benutzername'] = input("Benutzername: ")
    conf['token'] = input("Benutzertoken: ")
    conf['logfile'] = input("Logfile: ")
    conf['deviceId'] = input("Device-ID: ")
    conf['deviceName'] = input("Device Name: ")
    conf['deviceTyp'] = input("Device Typ: ")
    conf['deviceGroup'] = input("Device Gruppe: ")
    conf['deviceMainGrp'] = input("Device Hauptgruppe: ")
    conf['jsonDatei'] = input("JSON Inputdatei: ")
    conf['url'] = input("Sensorlogger URL: ")
    # conf['tempId'] = input("Temperatursensor ID: ")
    # conf['humidityId'] = input("Luftfeuchtigkeitssensor ID: ")

    while True:
        conf['anzahlsensoren'] = (input("Wieviele Sensoren sind vorhanden?: "))
        try:
            conf['anzahlsensoren'] = int(conf['anzahlsensoren'])
        except ValueError:
            print("Bitte eine Zahl eingeben!\n")
        else:
            break

    return conf


def sensordata(var):
    sensor = [[] for i in range(int(var))]
    sensor.append(var)
    for i in range(0, int(var)):
        sensor[i].append(i)
        sensor[i].append(input("Name von Sensor " + (str(int(i) + 1)) + ": "))
        sensor[i].append(input("Typ Sensor " + (str(int(i) + 1)) + ": "))
        sensor[i].append(input("Einheit von Sensor " + (str(int(i) + 1)) + ": "))
    return sensor


def createconf(configfile):
    if os.path.isfile(configfile):
        print("[Fehler] Konfigurationsdatei [%s] bereits vorhanden. Bitte gebe mit [-c neue.config] eine neue Konfigurationsdatei an." % configfile)
        sys.exit(1)
    else:
        data = userinput()
        sensor = sensordata(int(data['anzahlsensoren']))

        sensorlines = []
        sensorlines.append('')
        sensorlines.append('[SENSOREN]')
        sensorlines.append('anzahl = ' + str(data['anzahlsensoren']))
        sensorlines.append('')
        for i in range(0, int(data['anzahlsensoren'])):
            sensorlines.append('[SENSOR' + str(sensor[i][0]+1) + ']')
            sensorlines.append("name = " + str(sensor[i][1]))
            sensorlines.append("wert = " + str(sensor[i][2]))
            sensorlines.append("einheit = " + str(sensor[i][3]))
            sensorlines.append('')

        conflines = [
            '[USER]',
            'username = ' + str(data['benutzername']),
            'token = ' + str(data['token']),
            '',
            '[LOG]',
            'file = ' + str(data['logfile']),
            '',
            '[DEVICE]',
            'deviceId = ' + str(data['deviceId']),
            'deviceName = ' + str(data['deviceName']),
            'deviceTyp = ' + str(data['deviceTyp']),
            'deviceGroup = ' + str(data['deviceGroup']),
            'deviceMainGrp = ' + str(data['deviceMainGrp']),
            # 'tempID = ' + str(data['tempId']),
            # 'HumidityID = ' + str(data['humidityId']),
            '',
            '[DATA]',
            'input = ' + str(data['jsonDatei']),
            'logurl = ' + str(data['url']),
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
