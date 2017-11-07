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


config = configparser.ConfigParser()

if os.path.isfile(configfile):
    config.read(configfile)
else:
    print("[FEHLER] Configfile nicht vorhanden.")
    sys.exit(1)

# username = 'mluckau'  # Benutzername
username = config['USER']['username']
# token = 'gdBQD-dYkcZ-7QSxx-kKYQE-azoiC'  # Api-Token
token = config['USER']['token']
# json_file = "/var/www/html/json/current/current.json"  # JSON-file das die Sensordaten enthält
json_file = config['DATA']['input']
# deviceId = '6e653e48-0f9f-11e7-93ae-92361f002671'  # Die Device ID
deviceId = config['DEVICE']['deviceId']
# url = 'https://cloud.interitus.de/index.php/apps/sensorlogger/api/v1/createlog/'  # Posting URL für Sensorlogger
url = config['DATA']['url']
# logdatei = "/home/pi/sendjsondaten/senddata.log"  # Vollständiger Pfad und Dateiname zur Logdatei
logdatei = config['LOG']['file']
# rmjson = False  # soll das json-file nach jedem erfolgreichen übertragen gelöscht werden?
rmjson = config['DATA']['removejson']
# dataTypeIdTemp = 4  # Data Type ID für Temperatur
dataTypeIdTemp = config['DEVICE']['tempID']
# dataTypeIdHumidity = 5  # Data Type ID für Luftfeuchtigkeit
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

        # payload = {
        #	'deviceId': deviceId,
        #	'temperature': temp,
        #	'humidity': humidity,
        #	'date': currentDate
        # }

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