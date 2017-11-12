# -*- coding: utf-8 -*-
import os
import sys


def userinput():
    conf = {}
    while True:
        conf['benutzername'] = input("Benutzername: ")
        if len(str(conf['benutzername'])) == 0:
            print("Bitte einen Benutzernamen eingeben!")
        else:
            break

    while True:
        conf['token'] = input("Benutzertoken: ")
        if len(str(conf['token'])) == 0:
            print("Bitte den Benutzertoken für den Benutzer[" + conf['benutzername'] + "] eingeben!")
        else:
            break

    while True:
        conf['logfile'] = input("Logfile: ")
        if len(str(conf['logfile'])) == 0:
            print("Bitte den Pfad/Dateinamen für das Logfile eingeben!")
        else:
            break

    while True:
        conf['deviceId'] = input("Device-ID: ")
        if len(str(conf['deviceId'])) == 0:
            print("Bitte die Device-ID eingeben!")
        else:
            break

    while True:
        conf['deviceName'] = input("Device Name: ")
        if len(str(conf['deviceName'])) == 0:
            print("Bitte den Device Namen eingeben!")
        else:
            break

    while True:
        conf['deviceTyp'] = input("Device Typ: ")
        if len(str(conf['deviceTyp'])) == 0:
            print("Bitte den Device Typ eingeben!")
        else:
            break

    while True:
        conf['deviceGroup'] = input("Device Gruppe: ")
        if len(str(conf['deviceGroup'])) == 0:
            print("Bitte die Device Gruppe eingeben!")
        else:
            break

    while True:
        conf['deviceMainGrp'] = input("Device Hauptgruppe: ")
        if len(str(conf['deviceMainGrp'])) == 0:
            print("Bitte die Hauptgruppe des Devices eingeben!")
        else:
            break

    while True:
        conf['jsonDatei'] = input("JSON Inputdatei: ")
        if len(str(conf['jsonDatei'])) == 0:
            print("Bitte den Pfad/Dateinamen für das Input JSON-File eingeben!")
        else:
            break

    while True:
        conf['url'] = input("Nextcloud URL: ")
        if len(str(conf['url'])) == 0:
            print("Bitte die URL zu deinem Nextcloud Server eingeben!")
        else:
            break
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
        sensor[i].append(input("Name vom Sensor " + (str(int(i) + 1)) + ": "))
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
