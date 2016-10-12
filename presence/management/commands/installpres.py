# -*- coding: utf-8 -*-

import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
import presence
from presence.management.conf import bcolors
from instant.conf import SECRET_KEY, CENTRIFUGO_HOST, CENTRIFUGO_PORT
from presence.conf import CHANNEL, FREQUENCY


class Command(BaseCommand):
    help = 'Installs the Django Presence go worker'

    def handle(self, *args, **options):
        prespath = os.path.dirname(presence.__file__)
        gomodpath = os.path.join(prespath, 'go')
        # copy the executable
        print "Installing the worker ..."
        _cmd = "cp -v "+gomodpath+"/centpres "+settings.BASE_DIR
        os.system(_cmd)
        print "["+bcolors.OKBLUE+"x"+bcolors.ENDC+"] Executable file installed" 
        # generate config
        print "Generating config ..."
        conf = {
                "centrifugo_secret_key":SECRET_KEY,
                "centrifugo_host":CENTRIFUGO_HOST,
                "centrifugo_port":str(CENTRIFUGO_PORT),
                "channels":[CHANNEL],
                "frequency":FREQUENCY
                }
        _file = open(settings.BASE_DIR+"/centpres_config.json", "w")
        _file.write(json.dumps(conf))
        _file.close()
        print "["+bcolors.OKBLUE+"x"+bcolors.ENDC+"] File centpres_config.json generated" 
        msg = "[ "+bcolors.OKGREEN+"ok"+bcolors.ENDC+" ] Django presence worker installed: run "+bcolors.OKBLUE+"./centpres"+bcolors.ENDC+" to start the service"
        print msg
        return