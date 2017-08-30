from __future__ import print_function
import time
from datetime import datetime
from cent import Client
from django.core.management.base import BaseCommand
from instant.producers import publish
from instant.conf import CENTRIFUGO_HOST, CENTRIFUGO_PORT, SECRET_KEY
from presence.conf import WATCH_CHANNELS, PUBLISH_CHANNEL, FREQUENCY, TABS


def package(dataset, channel):
    anonymous = 0
    users = []
    tabs = {}
    for datapoint in dataset:
        user = dataset[datapoint]["user"]
        if user == "anonymous":
            anonymous += 1
        else:
            if user not in users:
                users.append(user)
            else:
                if TABS is True:
                    if user in tabs:
                        tabs["user"] = tabs["user"] + 1
                    else:
                        tabs["user"] = 2
    datapack = {"anonymous": anonymous, "users": users,
                "channel": channel}
    if TABS is True:
        datapack["tabs"] = tabs
    return datapack


class Command(BaseCommand):
    help = 'Runs the Django Presence worker'

    def add_arguments(self, parser):
        parser.add_argument('--v',
                            dest='verbosity',
                            default=1,
                            help='Set the verbosity level',
                            )

    def handle(self, *args, **options):
        exit_msg = "\nPresence worker stopped"
        verbosity = options["verbosity"]
        if verbosity > 0:
            print("Starting presence worker: watching channels",
                  ",".join(WATCH_CHANNELS))
            print("Sending presence info every", FREQUENCY, "seconds")
        while True:
            try:
                cent_url = CENTRIFUGO_HOST + ":" + str(CENTRIFUGO_PORT)
                client = Client(cent_url, SECRET_KEY, timeout=1)
                for chan in WATCH_CHANNELS:
                    data = client.presence(chan)
                    datapack = package(data, chan)
                    num_users = len(datapack["users"])
                    usr = "user"
                    if num_users > 1:
                        usr = "users"
                    msg = "Channel " + chan + ": " + str(num_users) + \
                        " " + usr + " and " + str(datapack["anonymous"]) + " anonymous" + \
                        " online"
                    now = datetime.now().strftime('%H:%M:%S')
                    if verbosity > 0:
                        print(now, msg)

                publish("", "__presence__", datapack, PUBLISH_CHANNEL)
                time.sleep(FREQUENCY)
            except KeyboardInterrupt:
                if verbosity > 0:
                    print(exit_msg)
                return
            except:
                if verbosity > 0:
                    print(exit_msg)
                return
