from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from constants import *

def createKeyboard(items):
	""" Takes list of labels (commands) (or list of lists of labels) and returns ReplyKeyboardMarkup"""
	ret = [0] * len(items)
	for i, it in enumerate(items):
		if type(it) == str:
			ret[i] = [KeyboardButton(it)]
			continue
		ret[i] = [0] * len(it)
		for j, it2 in enumerate(it):
			ret[i][j] = KeyboardButton(it2)
	return ReplyKeyboardMarkup(ret)

# MarkUp keyboards for different replies
mup_start = createKeyboard([['/start'], ['/list']])
mup_pause_stop = createKeyboard([['/pause', '/stop'], ['/list']])
mup_resume_stop = createKeyboard([['/resume', '/stop'], ['/list']])

imup_list_update = InlineKeyboardMarkup([[InlineKeyboardButton('Refresh', callback_data=1)]])