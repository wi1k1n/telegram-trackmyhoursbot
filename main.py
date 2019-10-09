#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging

import telegram as tg
from telegram import InlineKeyboardButton as ikbtn, InlineKeyboardMarkup as ikbmkp
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters

import dbhandler as dbh
from api_token import TOKEN as TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


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
	# logger.info("check_leave_group()")
	if not update.message.chat.type == update.message.chat.PRIVATE:
		logger.warning("Added to group! Leaving..")
		update.message.bot.leave_chat(update.message.chat_id)

def start(update, context):
	chat_id = update.message.chat_id
	keyboard = None
	reply_msg = ''
	chat_exist = dbh.chat_exists(chat_id)
	if (chat_exist):
		tasks = dbh.get_tasks_list(chat_id)
		if (len(tasks) == 0):
			reply_msg = 'You can track your time here. ' \
						'You have not added any timers yet. ' \
						'Use the following buttons to do that:'
			keyboard = create_keyboard([[('Start timer', '/new'), ('Add manually', '/add')],
										[('/help', '/help')]])
		else:
			reply_msg = 'You can track your time here.\n' \
						'You have {0} timers. Please choose action:'.format(len(tasks))
			keyboard = create_keyboard([[('Delete all data', '/destroy')],
										[('Start timer', '/new'), ('List timers', '/list'), ('Add manually', '/add')],
										[('/help', '/help')]])
	else:
		# TODO: handle DB-errors
		dbh.create_chat(chat_id)
		tasks = dbh.get_tasks_list(chat_id)
		if (len(tasks) == 0):
			reply_msg = 'Welcome! You can track your time here. Please choose action:'
			keyboard = create_keyboard([[('Start timer', '/new'), ('Add manually', '/add')],
										[('/help', '/help')]])
		else:
			reply_msg = 'Welcome back! You can track your time here.\n' \
						'There are some data left from your previous session.\n' \
						'You have {0} timers. Please choose action:'.format(len(tasks))
			keyboard = create_keyboard([[('Delete all previous data', '/destroy')],
										[('Start timer', '/new'), ('List timers', '/list'), ('Add manually', '/add')],
										[('/help', '/help')]])
	if keyboard:
		update.message.reply_text(reply_msg, reply_markup=ikbmkp(keyboard))
	else:
		update.message.reply_text(reply_msg)

def list(update, context):
	chat_id = update.message.chat_id
	tasks = dbh.get_tasks_list(chat_id)

	reply_msg = 'You have {0} timers:'.format(len(tasks))
	for task in tasks:
		reply_msg += '\n{0}: {1} -> {2}'.format('Unlabeled' if len(task.label) == 0 else task.label,
												task.start,
												'Now' if task.end is None else task.end)
	update.message.reply_text(reply_msg)

def new(update, context):
	# update.message.reply_text("WARNING: Function 'new' is not implemented yet!")

	task = dbh.create_task(update.message.chat_id)

	reply_msg = 'You have created a timer starting at {0}.\n' \
				'You can label this timer, pick a category or set the time of end'.format(task.start)
	keyboard = create_keyboard([[('Label', '/label'), ('Category', '/category'), ('Set end', '/end')],
								[('Start new timer', '/new'), ('List timers', '/list'), ('Add manually', '/add')]])
	update.message.reply_text(reply_msg, reply_markup=ikbmkp(keyboard))

def pause(update, context):
	update.message.reply_text("WARNING: Function 'pause' is not implemented yet!")

def resume(update, context):
	update.message.reply_text("WARNING: Function 'resume' is not implemented yet!")

def stop(update, context):
	update.message.reply_text("WARNING: Function 'stop' is not implemented yet!")

def add(update, context):
	update.message.reply_text("WARNING: Function 'add' is not implemented yet!")

def destroy(update, context):
	update.message.reply_text("WARNING: Function 'destroy' is not implemented yet!")

def about(update, context):
	update.message.reply_text("WARNING: Function 'about' is not implemented yet!")


def button(update, context):
	query = update.callback_query

	query.edit_message_text(text="Selected option: {}".format(query.data))



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
	# dp.add_handler(tg.ext.MessageHandler(Filters.status_update.new_chat_members, check_leave_group))

	dp.add_handler(CommandHandler('help', help), group=1)
	dp.add_handler(CommandHandler('start', start), group=1)
	dp.add_handler(CommandHandler('list', list), group=1)
	dp.add_handler(CommandHandler('new', new), group=1)
	dp.add_handler(CommandHandler('add', add), group=1)
	dp.add_handler(CommandHandler('pause', pause), group=1)
	dp.add_handler(CommandHandler('resume', resume), group=1)
	dp.add_handler(CommandHandler('stop', stop), group=1)
	dp.add_handler(CommandHandler('destroy', destroy), group=1)
	dp.add_handler(CommandHandler('about', destroy), group=1)

	dp.add_handler(CallbackQueryHandler(button), group=1)
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()