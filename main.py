#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Bot which sets up timers (with pauses) and keeps history of finished timers
"""

from telegram.ext import Updater, Filters, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler
from api_token import TOKEN
from handlers import *

def main():
	updater = Updater(TOKEN, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(ConversationHandler(
		entry_points=[
			CommandHandler(CMD_START, welcome)
		],
		states={
			STATE_WAIT_FOR_START: [
				CommandHandler(CMD_START, start),
				CommandHandler(CMD_LIST, ls)
			],
			STATE_RUNNING: [
				CommandHandler(CMD_PAUSE, pause),
				CommandHandler(CMD_STOP, stop),
				CommandHandler(CMD_LIST, ls)
			],
			STATE_PAUSED: [
				CommandHandler(CMD_RESUME, resume),
				CommandHandler(CMD_STOP, stop),
				CommandHandler(CMD_LIST, ls)
			]
		},
		fallbacks=[]
	))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()