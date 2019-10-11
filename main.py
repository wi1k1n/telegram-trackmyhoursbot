#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
TrackMyHours
"""
import logging

import telegram as tg
from telegram import InlineKeyboardButton as ikbtn, InlineKeyboardMarkup as ikbmkp
from telegram import KeyboardButton as kbtn, ReplyKeyboardMarkup as rkbmkp
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, ConversationHandler, MessageHandler

import dbhandler as dbh
from api_token import TOKEN as TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

IDLE, LIST_TASKS, TASK_CHANGE_MENU, TASK_CHANGE_SPECIFY, SETTINGS, STATISTICS = range(6)

BTN_START = '⏱ Start'
BTN_STOP = '⏹ Stop'
BTN_ADD = '➕ Add'
BTN_LIST = '📃 List'
BTN_SETTINGS = '⚙ Settings'
BTN_CATEGORY = 'Category'
BTN_DESCRIPTION = 'Description'
BTN_CHANGE_START = 'Change Start'
BTN_CHANGE_END = 'Change End'
BTN_DELETE = 'Delete'
BTN_BACK = 'Back'
BTN_TO_MENU = 'To Main Menu'
BTN_CANCEL = 'Cancel'
BTN_NOW = 'Now'
BTN_5M = '5m'
BTN_15M = '15m'
BTN_30M = '30m'
BTN_1H = '1h'

# Takes an array of tuples (or of arrays of tuples) of form ('label', 'action')
# and returns an array of InlineKeyboardButtons
def create_keyboard(arr):
	return [(ikbtn(row[0], callback_data=row[1])
			 if type(row) is tuple
			 else [ikbtn(el[0], callback_data=el[1])
				   for el in row])
			for row in arr]


def help(update, context):
	update.message.reply_text("Track your time with this bot.\n\n"
								"You have 0 running tasks!\n\n"
								"The following commands are available:\n"
								"/help  -  shows this information\n"
								"/start  -  starts bot from the very beginning\n"
								"/list  -  shows list of running tasks\n"
								"/new  -  starts new task\n"
								"/add  -  adds new task\n"
								"/pause  -  pauses currently running task\n"
								"/resume  -  resumes currently paused task\n"
								"/stop  -  stops currently runing task\n"
								"/destroy  -  destroy all stored information")

# Leave groups/channels and stay only in private chats
def check_leave_group(update, context):
	if not update.message.chat.type == update.message.chat.PRIVATE:
		logger.warning("Added to group #{0}! Leaving...".format(update.message.chat_id))
		update.message.bot.leave_chat(update.message.chat_id)

# Entry point to bot
def start(update, context):
	chat_id = update.message.chat_id

	# Add new chat_id to DB
	if dbh.chat_exists(chat_id) == 0:
		chat = dbh.create_chat(chat_id)
		if chat > 1:
			logger.warning('Error while inserting new chat #{0} into DB: returned value {1}'.format(chat_id, chat))

	markup = rkbmkp([[BTN_START, BTN_STOP],
					[BTN_ADD, BTN_LIST],
					[BTN_SETTINGS]],
					one_time_keyboard=True)
	update.message.reply_text('Welcome! You can track your time here. Choose option from menu to start.', reply_markup=markup)
	return IDLE

# Handles actions [Start] and [New] and offers options to tune task properties
def task_change_menu(upd, ctx):
	chat_id = upd.message.chat_id
	text = upd.message.text
	

	if text == BTN_START:
		task = dbh.create_task(chat_id)
		if task is None:
			logger.warning('Error while inserting new task into DB. Returned \'None\'')
			upd.message.reply_text('Internal error occured on server. This case has already been reported. Please try again later.')
		else:
			keyboard = [[BTN_CHANGE_START, BTN_CHANGE_END],
						[BTN_CATEGORY, BTN_DESCRIPTION],
						[BTN_DELETE, BTN_BACK, BTN_TO_MENU]]
			markup = rkbmkp(keyboard, one_time_keyboard=True)
			upd.message.reply_text('Task has been already started at {0}.\n'
								   'Use menu options to give more information'.format(task.start),
								   reply_markup=markup)
			return TASK_CHANGE_MENU
	pass

# Responsible for requesting change information from user
def task_change_specify(upd, ctx):
	chat_id = upd.message.chat_id
	text = upd.message.text

	if text == BTN_CHANGE_START:
		markup = rkbmkp([[BTN_NOW, BTN_5M, BTN_15M, BTN_1H],
						[BTN_CANCEL]],
						one_time_keyboard=True)
		upd.message.reply_text('Please set (date)time, when task started:',
							   reply_markup=markup)
		return TASK_CHANGE_SPECIFY
	pass

# Parses user's information
def task_change(upd, ctx):
	chat_id = upd.message.chat_id
	text = upd.message.text


	pass

def debug_msg_blank(update, context):
	""" Temporary message handler which just repeats what it gets """
	text = update.message.text
	update.message.reply_text(text)

def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(TOKEN, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(tg.ext.MessageHandler(Filters.all, check_leave_group), group=0)

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],

		states={
			IDLE: [MessageHandler(Filters.regex('^({0}|{1})$'.format(BTN_START, BTN_ADD)), task_change_menu)],

			TASK_CHANGE_MENU: [MessageHandler(Filters.regex('^({0}|{1}|{2}|{3}|{4})$'
															.format(BTN_CHANGE_START, BTN_CHANGE_END, BTN_CATEGORY, BTN_DESCRIPTION, BTN_DELETE)),
											  task_change_specify)],

			TASK_CHANGE_SPECIFY: [MessageHandler(Filters.text, task_change)],
		},

		fallbacks=[MessageHandler(Filters.text, debug_msg_blank)]
	)
	dp.add_handler(conv_handler, group=1)

	# dp.add_handler(CallbackQueryHandler(button), group=1)
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()