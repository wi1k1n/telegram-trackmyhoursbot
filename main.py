#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging

import telegram as tg
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters

from dbhandler import DBHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

dbh = DBHandler("main.db")


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
	tasks = dbh.get_task_list(update.message.chat_id)
	if tasks is None:
		update.message.reply_text('An error occurred. Please try again later')
		return
	msg = 'You have {0} tasks'.format(len(tasks))
	keyboard = [[tg.InlineKeyboardButton("1", callback_data='1'),
				tg.InlineKeyboardButton("2", callback_data='2')],

				[tg.InlineKeyboardButton("3", callback_data='3')]]

	reply_markup = tg.InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Please choose:', reply_markup=reply_markup)

def list(update, context):
	# update.message.reply_text("WARNING: Function 'list' is not implemented yet!")

	err, tasks = dbh.get_task_list(update.message.chat_id)
	if err != 0:
		update.message.reply_text("An error occurred on server. This case has already been reported. Please, come back later!")

	for task in tasks:
		logger.info(task)

def new(update, context):
	# update.message.reply_text("WARNING: Function 'new' is not implemented yet!")

	dbh.create_task(update.message.chat_id)

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



def initialize_db(dbh):
	dbh.create_table_tasks()

def main():
	# Initializes database, creates all necessary tables if needed
	initialize_db(dbh)

	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater("936170346:AAEs2IYkJNiMJBoBDUSX4-if10fOYTRQH5A", use_context=True)
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