# -*- coding: utf-8 -*-
import os
import sys


conflines = [
    '[USER]',
    'username = ',
    'token = ',
    '',
    '[LOG]',
    'file = senddata.log',
    '',
    '[DEVICE]',
    'deviceId = ',
    'tempID = ',
    'HumidityID = ',
    '',
    '[DATA]',
    'input = /var/www/html/json/current/current.json',
    'url = https://deine.nextcloud.url/index.php/apps/sensorlogger/api/v1/createlog/',
    'removejson = False'
]


def createconf(configfile):
    if os.path.isfile(configfile):
        print("[Fehler] Konfigurationsdatei [%s] bereits vorhanden." % configfile)
        sys.exit(1)
    else:
        try:
            with open(configfile, 'w') as config:
                config.write('\n'.join(conflines))
            print("[OK] Konfigurationsdatei [%s] erstellt. Bitte passe sie an deine Umgebung an." % configfile)
            sys.exit(0)
        except IOError as e:
            print(("[Fehler] Konfigurationsdatei [%s] konnte nicht geschrieben werden. [%s]" % (configfile, e.strerror)))
            sys.exit(1)
