import logging, re
import numpy as np
from telegram import ParseMode
from telegram.ext import Updater, Filters, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler
from constants import *
from keyboards import *
from util import *
from modules.user import User, State

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TrackMyHoursBot:
	def __init__(self, token, dataManager):
		self.token = token
		self.dm = dataManager
		self.updater = None

	def startBot(self, blockThread=True):
		self.updater = Updater(self.token, use_context=True)
		dp = self.updater.dispatcher

		dp.add_handler(ConversationHandler(
			entry_points=[
				CommandHandler(CMD_START, self.welcomeHandler),
				CommandHandler(CMD_RESUME, self.resumeHandler),
				CommandHandler(CMD_PAUSE, self.pauseHandler),
				CommandHandler(CMD_STOP, self.stopHandler),
				CommandHandler(CMD_LIST, self.lsHandler),
				CommandHandler(CMD_CLEAR, self.clearHandler),
				CommandHandler(CMD_HELP, self.helpHandler),
				CallbackQueryHandler(self.callBackQueryHandler),
				MessageHandler(Filters.all, self.welcomeHandler)
			],
			states={
				STATE_WAIT_FOR_START: [
					CommandHandler(CMD_START, self.startHandler),
					CommandHandler(CMD_PAUSE, self.pauseHandler),
					CommandHandler(CMD_RESUME, self.resumeHandler),
					CommandHandler(CMD_STOP, self.stopHandler),
					CommandHandler(CMD_LIST, self.lsHandler),
					CommandHandler(CMD_CLEAR, self.clearHandler),
					CommandHandler(CMD_HELP, self.helpHandler),
					CallbackQueryHandler(self.callBackQueryHandler),
				],
				STATE_RUNNING: [
					CommandHandler(CMD_START, self.startHandler),
					CommandHandler(CMD_PAUSE, self.pauseHandler),
					CommandHandler(CMD_RESUME, self.resumeHandler),
					CommandHandler(CMD_STOP, self.stopHandler),
					CommandHandler(CMD_LIST, self.lsHandler),
					CommandHandler(CMD_CLEAR, self.clearHandler),
					CommandHandler(CMD_HELP, self.helpHandler),
					CallbackQueryHandler(self.callBackQueryHandler),
				],
				STATE_PAUSED: [
					CommandHandler(CMD_START, self.startHandler),
					CommandHandler(CMD_PAUSE, self.pauseHandler),
					CommandHandler(CMD_RESUME, self.resumeHandler),
					CommandHandler(CMD_STOP, self.stopHandler),
					CommandHandler(CMD_LIST, self.lsHandler),
					CommandHandler(CMD_CLEAR, self.clearHandler),
					CommandHandler(CMD_HELP, self.helpHandler),
					CallbackQueryHandler(self.callBackQueryHandler),
				],
				STATE_WAIT_CLEAR_APPROVAL: [
					MessageHandler(Filters.regex(re.compile(r'yes', re.IGNORECASE)), self.finallyClearHandler),
					CallbackQueryHandler(self.callBackQueryHandler),
					MessageHandler(Filters.all, self.abortClearHandler),
				]
			},
			fallbacks=[]
		))

		# log all errors
		dp.add_error_handler(self.errorHandler)

		# Start the Bot
		self.updater.start_polling()

		if blockThread:
			# Run the bot until you press Ctrl-C or the process receives SIGINT,
			# SIGTERM or SIGABRT. This should be used most of the time, since
			# start_polling() is non-blocking and will stop the bot gracefully.
			self.updater.idle()

	def stopBot(self):
		self.updater.stop()
		self.updater = None
		self.dm.save()


	def welcomeHandler(self, upd, ctx):
		""" Called at the very beginning by /start. """
		logger.debug('>> welcomeHandler(upd, ctx)')

		# simply start timer if user already exists
		if self.dm.hasUser(upd.effective_user):
			usr = self.dm[upd.effective_user.id]
			initialState = usr.state
			ts = usr.startTimer()
			if initialState == State.PAUSED or initialState == State.RUNNING:
				(_, w, _, p, _, _) = usr.getStatistics()
				reply = MSGC_JOBRESUMED.format(formatSeconds(w), formatSeconds(p))
			else:
				reply = MSGC_JOBSTARTED.format(formatTimeStamp(ts, 'full'))
			upd.message.reply_text(reply, reply_markup=mup_pause_stop)
			return STATE_RUNNING

		self.dm.addUser(upd.effective_user)

		# Send welcome message
		msg = upd.message.reply_text(MSGC_WELCOME, reply_markup=mup_start)
		return STATE_WAIT_FOR_START

	def startHandler(self, upd, ctx):
		""" Called by command /start """
		logger.debug('>> startHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)

		usr = self.dm[upd.effective_user.id]
		initialState = usr.state
		ts = usr.startTimer()
		if initialState == State.PAUSED or initialState == State.RUNNING:
			(_, w, _, p, _, _) = usr.getStatistics()
			reply = MSGC_JOBRESUMED.format(formatSeconds(w), formatSeconds(p))
		else:
			reply = MSGC_JOBSTARTED.format(formatTimeStamp(ts, 'full'))
		upd.message.reply_text(reply, reply_markup=mup_pause_stop)
		return STATE_RUNNING

	def pauseHandler(self, upd, ctx):
		""" Called by command /pause """
		logger.debug('>> pauseHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)

		usr = self.dm[upd.effective_user.id]
		initialState = usr.state
		ts = usr.pauseTimer()
		(_, w, _, p, _, _) = usr.getStatistics()
		if initialState == State.PAUSED:
			reply = MSGC_JOBALREADYPAUSED.format(formatSeconds(w), formatSeconds(p))
			upd.message.reply_text(reply, reply_markup=mup_resume_stop)
			return STATE_PAUSED
		elif initialState == State.STOPPED:
			reply = MSGC_JOBALREADYSTOPPEDFORPAUSE
			upd.message.reply_text(reply, reply_markup=mup_start)
			return STATE_WAIT_FOR_START
		else:
			reply = MSGC_JOBPAUSED.format(formatSeconds(w), formatSeconds(p))
			upd.message.reply_text(reply, reply_markup=mup_resume_stop)
			return STATE_PAUSED

	def resumeHandler(self, upd, ctx):
		""" Called by command /resume """
		logger.debug('>> resumeHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)

		usr = self.dm[upd.effective_user.id]
		initialState = usr.state
		ts = usr.startTimer()
		(_, w, _, p, _, _) = usr.getStatistics()
		if initialState == State.PAUSED:
			reply = MSGC_JOBRESUMED.format(formatSeconds(w), formatSeconds(p))
		elif initialState == State.RUNNING:
			reply = MSGC_JOBALREADYRUNNING.format(formatSeconds(w), formatSeconds(p))
		else:
			reply = MSGC_JOBSTARTED.format(formatTimeStamp(ts, 'full'))

		upd.message.reply_text(reply, reply_markup=mup_pause_stop)
		return STATE_RUNNING

	def stopHandler(self, upd, ctx):
		""" Called by command /stop """
		logger.debug('>> stopHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)

		usr = self.dm[upd.effective_user.id]
		initialState = usr.state
		ts = usr.stopTimer()
		(_, w, _, p, pn, _) = usr.getStatistics()
		if initialState == State.PAUSED or initialState == State.RUNNING:
			reply = MSGC_JOBSTOPPED.format(formatSeconds(w), pn, formatSeconds(p))
		else:
			reply = MSGC_JOBALREADYSTOPPED

		upd.message.reply_text(reply, reply_markup=mup_start)
		return STATE_WAIT_FOR_START

	def getListTracksData(self, usr):
		reply = ''
		for i in range(len(usr.tracks)):
			tsStart, timeWork, _, timePause, _, state = usr.getStatistics(i)
			reply += ('>' if state == State.RUNNING else '#') + ' [' + formatTimeStamp(tsStart, 'date') + '] ' + \
					 formatTimeStamp(tsStart, 'time') + ' => ' + formatSeconds(timeWork) + \
					 ' / ' + formatSeconds(timePause) + '\n'
		return reply.strip()

	def lsHandler(self, upd, ctx):
		""" Called by command /ls """
		logger.debug('>> lsHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)

		usr = self.dm[upd.effective_user.id]
		reply = self.getListTracksData(usr)
		if not reply:
			upd.message.reply_text(MSGC_LSNOTRACKSYET, reply_markup=mup_start)
			return
		# upd.message.reply_text('Command /list is not implemented yet!')
		upd.message.reply_text(reply, reply_markup=imup_list_update)

	def callBackQueryHandler(self, upd, ctx):
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)
		query = upd.callback_query
		query.answer()
		usr = self.dm[upd.effective_user.id]
		reply = self.getListTracksData(usr)
		if not reply:
			query.edit_message_text(MSGC_LSNOTRACKSYET)
			return
		if (upd.effective_message.text.strip() != reply):
			query.edit_message_text(reply, reply_markup=imup_list_update)

	def clearHandler(self, upd, ctx):
		""" Called by command /clear """
		logger.debug('>> clearHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)
		usr = self.dm[upd.effective_user.id]
		if len(usr.tracks):
			upd.message.reply_text(MSGC_CLEARWARNING.format(len(self.dm[upd.effective_user.id].tracks)))
			return STATE_WAIT_CLEAR_APPROVAL

		upd.message.reply_text(MSGC_CLEARNODATA)
		return STATE_WAIT_FOR_START

	def finallyClearHandler(self, upd, ctx):
		""" Called by answering 'yes' after /clear command """
		logger.debug('>> finallyClearHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)
		self.dm[upd.effective_user.id].tracks = []
		upd.message.reply_text(MSGC_CLEARSUCCESS)
		return STATE_WAIT_FOR_START
	def abortClearHandler(self, upd, ctx):
		""" Called by NOT answering 'yes' after /clear command """
		logger.debug('>> finallyClearHandler(upd, ctx)')
		self.dm.hasUser(upd.effective_user, addIfNotExists=True)
		upd.message.reply_text(MSGC_CLEARABORT)
		return STATE_WAIT_FOR_START

	def helpHandler(self, upd, ctx):
		""" Called by command /help """
		logger.debug('>> helpHandler(upd, ctx)')
		upd.message.reply_text(MSGC_HELP)


	def errorHandler(self, upd, ctx):
		"""Log Errors caused by Updates."""
		logger.warning('Update "%s" caused error "%s"', upd, ctx.error)




	def isStopped(self):
		return self.updater is None