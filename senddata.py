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


### Konfiguration ###

configfile = './config.file'

if os.path.isfile(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
else:
    print("[FEHLER] Configfile nicht vorhanden.")
    sys.exit(1)

username = config['USER']['username']
token = config['USER']['token']
json_file = config['DATA']['input']
deviceId = config['DEVICE']['deviceId']
url = config['DATA']['url']
logdatei = config['LOG']['file']
rmjson = config['DATA']['removejson']
dataTypeIdTemp = config['DEVICE']['tempID']
dataTypeIdHumidity = config['DEVICE']['humidityID']


### Ab hier sind keine Änderungen mehr notwendig ###

def log(msg):
    try:
        file = open(logdatei, "a")
        file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
        file.close
    except IOError as e:
        print(("[Warnung] Logdatei [%s] konnte nicht geschrieben werden. [%s]" % (logdatei, e.strerror)))
        print(("%s" % msg))

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

        req = urllib.request.Request(url)
        base64string = base64.encodestring('%s:%s' % (username, token)).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header("Content-Security-Policy",
                       "default-src 'none';script-src 'self' 'unsafe-eval';style-src 'self' 'unsafe-inline';img-src 'self' data: blob:;font-src 'self';connect-src 'self';media-src 'self'")
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(payload)

        try:
            response = urllib.request.urlopen(req, data)
            result = response.getcode()

            if bparameter:
                log("[OK] Wetterdaten erfolgreich an Server gesendet.[t: %s][h: %s][Responsecode: %s][Trigger: %s]" % (
                temp, humidity, result, parameter))
            else:
                log("[OK] Wetterdaten erfolgreich an Server gesendet.[t: %s][h: %s][Responsecode: %s]" % (
                temp, humidity, result))

        except urllib.error.HTTPError as e:
            log("[Fehler] Daten konnten nicht an Server gesendet werden. [Fehlercode: %s]" % e.code)
            sys.exit(1)

        if rmjson:
            removeJson()
        else:
            sys.exit(0)

    else:
        log("[Fehler] %s konnte nicht gelesen werden." % json_file)
        sys.exit(1)


if sys.argv[1:]:  # Überprüfen ob Kommandozeilenparameter übergeben wurden
    parameter = sys.argv[1]
    bparameter = True
else:
    bparameter = False

if os.path.isfile(json_file):
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    temp = ('%.1f' % float((data['stats']['current']['outTemp'].replace(',', '.'))))
    humidity = ('%.1f' % float((data['stats']['current']['humidity'].replace(',', '.'))))
    wetterdaten()
else:
    log("[Fehler] %s nicht vorhanden." % json_file)
    sys.exit(1)