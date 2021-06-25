#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Bot which sets up timers (with pauses) and keeps history of finished timers
"""

from configuration import TOKEN, DB_PATH
from modules.trackmyhoursbot import TrackMyHoursBot
from modules.datamanager import DataManager

if __name__ == '__main__':
	bot = TrackMyHoursBot(TOKEN, DataManager(DB_PATH))
	bot.startBot()