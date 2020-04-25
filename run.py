#! /usr/bin/env python3

import logging
from web_app import web_app_ui

## Current output status for messages.
logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
	web_app_ui.start()