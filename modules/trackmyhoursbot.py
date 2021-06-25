import logging
from telegram import ParseMode
from telegram.ext import Updater, Filters, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler
from constants import *
from keyboards import *
from util import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TrackMyHoursBot:
	def __init__(self, token, dataManager):
		self.token = token
		self.dataManager = dataManager

	def startBot(self):
		updater = Updater(self.token, use_context=True)
		dp = updater.dispatcher

		dp.add_handler(ConversationHandler(
			entry_points=[
				CommandHandler(CMD_START, self.welcomeHandler)
			],
			states={
				STATE_WAIT_FOR_START: [
					CommandHandler(CMD_START, self.startHandler),
					CommandHandler(CMD_LIST, self.lsHandler)
				],
				STATE_RUNNING: [
					CommandHandler(CMD_PAUSE, self.pauseHandler),
					CommandHandler(CMD_STOP, self.stopHandler),
					CommandHandler(CMD_LIST, self.lsHandler)
				],
				STATE_PAUSED: [
					CommandHandler(CMD_RESUME, self.resumeHandler),
					CommandHandler(CMD_STOP, self.stopHandler),
					CommandHandler(CMD_LIST, self.lsHandler)
				]
			},
			fallbacks=[]
		))

		# log all errors
		dp.add_error_handler(self.errorHandler)

		# Start the Bot
		updater.start_polling()

		# Run the bot until you press Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		updater.idle()


	def startTimer(self, upd, ctx):
		usr = self.dataManager[upd.effective_user.id]
		ts = usr.startTimer()
		upd.message.reply_text(MSGC_JOBSTARTED.format(formatTimeStamp(ts, 'full')), reply_markup=mup_pause_stop)


	def welcomeHandler(self, upd, ctx):
		""" Called at the very beginning by /start. """
		logger.debug('>> welcome(upd, ctx)')

		# simply start timer if user already exists
		if self.dataManager.hasUser(upd.effective_user):
			self.startTimer(upd, ctx)
			return STATE_WAIT_FOR_START

		self.dataManager.addUser(upd.effective_user)

		# Send welcome message
		msg = upd.message.reply_text(MSGC_WELCOME, reply_markup=mup_start)
		return STATE_WAIT_FOR_START

	def startHandler(self, upd, ctx):
		""" Called by command /start """
		logger.debug('>> start(upd, ctx)')

		if not self.dataManager.hasUser(upd.effective_user):
			self.dataManager.addUser(upd.effective_user)

		self.startTimer(upd, ctx)
		return STATE_RUNNING

	def pauseHandler(self, upd, ctx):
		""" Called by command /pause """
		logger.debug('>> pause(upd, ctx)')

		if not self.dataManager.hasUser(upd.effective_user):
			self.dataManager.addUser(upd.effective_user)

		usr = self.dataManager[upd.effective_user.id]
		ts = usr.pauseTimer()

		upd.message.reply_text(MSGC_JOBPAUSED.format(formatTimeStamp(ts, 'time')), reply_markup=mup_resume_stop)

		return STATE_PAUSED

	def resumeHandler(self, upd, ctx):
		""" Called by command /resume """
		logger.debug('>> resume(upd, ctx)')

		if not self.dataManager.hasUser(upd.effective_user):
			self.dataManager.addUser(upd.effective_user)

		usr = self.dataManager[upd.effective_user.id]
		ts = usr.startTimer()

		upd.message.reply_text(MSGC_JOBRESUMED.format(formatTimeStamp(ts, 'time')), reply_markup=mup_pause_stop)

		return STATE_RUNNING

	def stopHandler(self, upd, ctx):
		""" Called by command /stop """
		logger.debug('>> stop(upd, ctx)')

		if not self.dataManager.hasUser(upd.effective_user):
			self.dataManager.addUser(upd.effective_user)

		usr = self.dataManager[upd.effective_user.id]
		ts = usr.stopTimer()

		upd.message.reply_text("Stopped!", reply_markup=mup_start)

		return STATE_WAIT_FOR_START


	def lsHandler(self, upd, ctx):
		""" Called by command /ls """
		logger.debug('>> ls(upd, ctx)')

		upd.message.reply_text('Command /list is not implemented yet!')


	def errorHandler(self, upd, ctx):
		"""Log Errors caused by Updates."""
		logger.warning('Update "%s" caused error "%s"', upd, ctx.error)