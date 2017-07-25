from __future__ import print_function
import argparse
import requests
import json
import signal
import sys

from groupmebot.session import Session, SessionException
from groupmebot.settings import Settings
from groupmebot.utils import *
# ^ private lib I use for my stats, will open source if interest


def buildSettings():

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="accessToken")
    args = vars(parser.parse_args())

    try:
        sessionSettings = Settings(file="config.json", **args)
    except Exception:
        raise SessionException("Running as module. Ensure config")

    return sessionSettings


def main():
    # Start logging
    setupLogger()
    logging.debug('Logger set up')

    # Load config
    sessionSettings = buildSettings()

    # Otherwise establish connection
    connection = requests.session()
    app = Session(sessionSettings, connection)

    # In here for scope
    def gracefulExit(signum, frame):
        connection.close()
        # Do logging instead here
        logging.info("Exiting...")
        sys.exit(0)

    # Handle abrupt endings
    signal.signal(signal.SIGINT, gracefulExit)

    _, data = app.getGroupById(21832576)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    main()
