# -*- coding: utf-8 -*-

import os
import sys
import time
import json
# import threading
import urllib.request, urllib.error, urllib.parse
import base64
from datetime import datetime
import configparser
import argparse
import createconf


parser = argparse.ArgumentParser(description="Sendet Weewx-Wetterdaten an einen Nextcloud-Server mit installierter Sensorlogger App.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--send", help="Daten senden [default]", action="store_true")
group.add_argument("-r", "--register", help="Device registrieren", action="store_true")
parser.add_argument("-d", "--debug", help="Debugmodus einschalten", action="store_true")
parser.add_argument("-c", "--config", help="Konfigurationsdatei [default = config.file]")
parser.add_argument("-e", "--econf", help="Konfigurationsdatei erzeugen", action="store_true")
parser.add_argument("-t", "--trigger", help="Incrontrigger übergabe zur Benutzung in der incrontab [z.B. senddata.py -t $%%] wird in Logdatei geschrieben zum debuggen.")
parser.add_argument("-l", "--logfile", help="Schreibt Ausgaben in [logfile], überschreibt die Angabe in der Konfigurationsdatei.")

args = parser.parse_args()


if args.config:
    configfile = args.config
else:
    configfile = './config.file'


if args.econf:
    createconf.createconf(configfile)


if os.path.isfile(configfile):
    config = configparser.ConfigParser(interpolation=None)
    config.read(configfile)
    username = config['USER']['username']
    token = config['USER']['token']
    json_file = config['DATA']['input']
    deviceId = config['DEVICE']['deviceId']
    deviceName = config['DEVICE']['deviceName']
    deviceType = config['DEVICE']['deviceTyp']
    deviceGroup = config['DEVICE']['deviceGroup']
    deviceMainGrp = config['DEVICE']['deviceMainGrp']
    sensoranzahl = config['SENSOREN']['anzahl']
    logurl = config['DATA']['logurl']

    if args.logfile:
        logdatei = args.logfile
    else:
        logdatei = config['LOG']['file']

    rmjson = config['DATA']['removejson']
    dataTypeIdTemp = config['DEVICE']['tempID']
    dataTypeIdHumidity = config['DEVICE']['humidityID']
else:
    print("[FEHLER] Configfile [%s] nicht vorhanden." % configfile)
    sys.exit(1)


if args.trigger:
    parameter = args.trigger
    bparameter = True
else:
    bparameter = False


def log(msg):
    try:
        file = open(logdatei, "a")
        file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
        file.close
        if args.debug:
            print(msg)
    except IOError as e:
        print(("[Warnung] Logdatei [%s] konnte nicht geschrieben werden. [%s]" % (logdatei, e.strerror)))
        print(("%s" % msg))


def sendjson(payload):
    req = urllib.request.Request(url)
    base64string = base64.encodebytes('%s:%s' % (username, token)).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header("Content-Security-Policy",
                   "default-src 'none';script-src 'self' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self' data: blob:;font-src 'self';connect-src 'self';media-src 'self'")
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(payload)

    try:
        response = urllib.request.urlopen(req, data)
        result = response.getcode()
        return result

    except urllib.error.HTTPError as e:
        log("[Fehler] Daten konnten nicht an Server gesendet werden. [Fehlercode: %s]" % e.code)
        sys.exit(1)


def removeJson():
    try:
        os.remove(json_file)
        log("[OK] %s gelöscht" % json_file)
        sys.exit(0)
    except OSError as e:
        log("[Warnung] %s konnte nicht gelöscht werden.[%s]" % (json_file, e.strerror))
        sys.exit(0)


def wetterdaten():
    cdatetime = datetime.now()
    currentGerDate = cdatetime.strftime('%d.%m.%Y %H:%M:%S')
    currentDate = cdatetime.strftime('%Y-%m-%d %H:%M:%S')

    if temp is not None and humidity is not None:

        payload = {
            'date': currentDate,
            'deviceId': deviceId,
            'data': [
                {
                    'dataTypeId': dataTypeIdTemp,
                    'value': temp
                },
                {
                    'dataTypeId': dataTypeIdHumidity,
                    'value': humidity
                }
            ]
        }

        result = sendjson(payload)

        if bparameter:
            log("[OK] Wetterdaten erfolgreich an Server gesendet.[t: %s][h: %s][Responsecode: %s][Trigger: %s]" % (
                temp, humidity, result, parameter))
        else:
            log("[OK] Wetterdaten erfolgreich an Server gesendet.[t: %s][h: %s][Responsecode: %s]" % (
                temp, humidity, result))

        if rmjson:
            removeJson()
        else:
            sys.exit(0)

    else:
        log("[Fehler] %s konnte nicht gelesen werden." % json_file)
        sys.exit(1)


def regdevice():
    # print("Device registrieren")
    # todo Code für Device Registrierung hinzufügen

    items = []
    for i in range(0, int(sensoranzahl)):
        items.append({})
        items[i]['type'] = config['SENSOR' + str(i+1)]['wert']
        items[i]['description'] = config['SENSOR' + str(i+1)]['name']
        items[i]['unit'] = str(config['SENSOR' + str(i+1)]["einheit"])

    payload = {}
    payload['deviceId'] = deviceId
    payload['deviceName'] = deviceName
    payload['deviceType'] = deviceType
    payload['deviceGroup'] = deviceGroup
    payload['deviceParentGroup'] = deviceMainGrp
    payload['deviceDataTypes'] = items
    test = json.dumps(payload, ensure_ascii=False)
    print("fertig")

if args.register:
    url = logurl + 'registerdevice/'
    regdevice()
else:
    if os.path.isfile(json_file):
        json_data = open(json_file)
        data = json.load(json_data)
        json_data.close()
        temp = ('%.1f' % float((data['stats']['current']['outTemp'].replace(',', '.'))))
        humidity = ('%.1f' % float((data['stats']['current']['humidity'].replace(',', '.'))))
        url = logurl + 'createlog/'
        wetterdaten()
    else:
        log("[Fehler] %s nicht vorhanden." % json_file)
        sys.exit(1)