import logging

from telegram import ParseMode

from constants import *
from keyboards import *
from util import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def welcome(upd, ctx):
	""" Called at the very beginning by /start. Initializes chat_data vars """
	logger.debug('>> welcome(upd, ctx)')

	# Set default values for ctx.chat_data dictionary
	ctx.chat_data[DK_JOBS] = {}
	ctx.chat_data[DK_CURJOB] = None

	# Send welcome message
	msg = upd.message.reply_text(MSGC_WELCOME, reply_markup=mup_start)

	return STATE_WAIT_FOR_START

def start(upd, ctx):
	""" Called by command /start """
	logger.debug('>> start(upd, ctx)')

	ts = curTimeStamp()
	ctx.chat_data[DK_CURJOB] = str(ts)

	# Create new entry in jobs dictionary
	curJob = ctx.chat_data[DK_CURJOB]
	ctx.chat_data[DK_JOBS][curJob] = {DK_TIMES: [ts], DK_STATISTICS: None}

	upd.message.reply_text(MSGC_JOBSTARTED.format(formatTimeStamp(ts, 'full')), reply_markup=mup_pause_stop)

	return STATE_RUNNING

def pause(upd, ctx):
	""" Called by command /pause """
	logger.debug('>> pause(upd, ctx)')

	ts = curTimeStamp()
	curJob = ctx.chat_data[DK_CURJOB]

	# Add current time entry
	ctx.chat_data[DK_JOBS][curJob][DK_TIMES].append(ts)

	upd.message.reply_text(MSGC_JOBPAUSED.format(formatTimeStamp(ts, 'time')), reply_markup=mup_resume_stop)

	return STATE_PAUSED

def resume(upd, ctx):
	""" Called by command /resume """
	logger.debug('>> resume(upd, ctx)')

	ts = curTimeStamp()
	curJob = ctx.chat_data[DK_CURJOB]

	# Add current time entry
	ctx.chat_data[DK_JOBS][curJob][DK_TIMES].append(ts)

	upd.message.reply_text(MSGC_JOBRESUMED.format(formatTimeStamp(ts, 'time')), reply_markup=mup_pause_stop)

	return STATE_RUNNING

def stop(upd, ctx):
	""" Called by command /stop """
	logger.debug('>> stop(upd, ctx)')

	ts = curTimeStamp()
	curJob = ctx.chat_data[DK_CURJOB]

	# Add current time entry
	ctx.chat_data[DK_JOBS][curJob][DK_TIMES].append(ts)


	# Calculate statistics
	timesList = ctx.chat_data[DK_JOBS][curJob][DK_TIMES]

	lastTimeStamp = 0
	totalJobTime = 0
	totalPauseTime = 0
	numberOfPauses = 0
	if len(timesList) < 2:  # Should never happen
		ctx.chat_data[DK_JOBS][curJob][DK_STATISTICS] = None
		logger.warning('{}<2 entries found in ctx.chat_data[DK_JOBS][str(ts)]!!'.format(len(timesList)))
	else:
		lastTimeStamp = timesList[0]
		jobTimeFlag = True
		for i in range(1, len(timesList)):
			timeDiff = timesList[i] - lastTimeStamp
			if jobTimeFlag: totalJobTime += timeDiff
			else:
				totalPauseTime += timeDiff
				numberOfPauses += 1
			lastTimeStamp = timesList[i]
			jobTimeFlag = not jobTimeFlag

		# Save statistics in ctx.chat_data
		ctx.chat_data[DK_JOBS][curJob][DK_STATISTICS] = {}
		ctx.chat_data[DK_JOBS][curJob][DK_STATISTICS][DK_TOTALJOBTIME] = totalJobTime
		ctx.chat_data[DK_JOBS][curJob][DK_STATISTICS][DK_TOTALPAUSETIME] = totalPauseTime
		ctx.chat_data[DK_JOBS][curJob][DK_STATISTICS][DK_NUMBERPAUSES] = numberOfPauses

	# Prepare messages to be replied
	msgReplyText = MSGC_JOBSTOPPED.format(formatTimeStamp(ts, 'full'), '', '')
	if lastTimeStamp != 0:  # Should always be True
		if numberOfPauses == 0:  # Short answer if no pauses
			msgReplyText = MSGC_JOBSTOPPED.format(formatTimeStamp(ts, 'full'),
												  formatSeconds(totalJobTime + totalPauseTime),
												  ' (0 pauses)')
		else:  # Long answer with totalPauseTime and numberOfPauses
			msgPausesExtra = MSGC_JOBSTOPPED_PAUSESEXTRA.format(formatSeconds(totalPauseTime),
																str(numberOfPauses),
																'pause' + ('' if numberOfPauses == 1 else 's'))
			msgWithoutPauses = MSGC_JOBSTOPPED_WITHOUTPAUSES.format(formatSeconds(totalJobTime))
			msgReplyText = MSGC_JOBSTOPPED.format(formatTimeStamp(ts, 'full'),
												  formatSeconds(totalJobTime + totalPauseTime),
												  msgPausesExtra + msgWithoutPauses)

	upd.message.reply_text(msgReplyText, reply_markup=mup_start)

	return STATE_WAIT_FOR_START


def ls(upd, ctx):
	""" Called by command /ls """
	logger.debug('>> ls(upd, ctx)')

	upd.message.reply_text('Command /list is not implemented yet!')


def error(upd, ctx):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', upd, ctx.error)