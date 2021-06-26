#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Bot which sets up timers (with pauses) and keeps history of finished timers
"""
from signal import signal, SIGINT, SIGTERM, SIGABRT
from time import sleep

from configuration import TOKEN, DB_PATH
from modules.trackmyhoursbot import TrackMyHoursBot
from modules.datamanager import DataManager

def cli(bot, dm):
	def help(bot, dm):
		ret = ''
		for cmdOption in cmds:
			ret += cmdOption[0][0] + '\t' + cmdOption[1] + '\n'
		print(ret)

	def exit(bot, dm):
		print('Please wait while the bot is stopping..')
		bot.stopBot()
		print('Stopped!')

	def list(bot, dm):
		print(str(len(dm.db.keys())) + ' users in total:')
		for id in dm.db.keys():
			usr = dm.db[id]
			print('[' + str(id) + '] ' + usr.firstName + ((' (@' + usr.username + ')') if usr.username else '') + '. ' + \
				  str(len(usr.tracks)) + ' tracks')

	def save(bot, dm):
		print('Saving database..')
		dm.save()
		print('Saved!')

	cmds = [
		[['help'], 'show this message', help],
		[['exit', 'quit', 'stop'], 'stop bot and exit program', exit],
		[['list'], 'list users in database', list],
		[['save'], 'save database to disk', save]
	]

	for sig in [SIGINT, SIGTERM, SIGABRT]:
		signal(sig, bot.stopBot)

	print('Welcome to TrackMyHoursBot CLI. Use help command to check all possible commands')

	is_idle = True
	while is_idle:
		print('> ', end='')
		inp = input()
		cmdFound = False
		for cmdOption in cmds:
			cmdList = cmdOption[0]
			for cmd in cmdList:
				if inp == cmd:
					cmdFound = True
					if cmdOption[-1]:
						cmdOption[-1](bot, dm)
					break
			if cmdFound:
				break
		if not cmdFound:
			print('Command not found. Use the following commands:')
			help(bot)

		if bot.isStopped():
			is_idle = False

if __name__ == '__main__':
	dm = DataManager(DB_PATH)
	bot = TrackMyHoursBot(TOKEN, dm)
	bot.startBot(blockThread=False)
	cli(bot, dm)