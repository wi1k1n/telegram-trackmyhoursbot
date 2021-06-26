# States for ConversationHangler
STATE_WAIT_FOR_START, \
STATE_RUNNING, \
STATE_PAUSED, \
STATE_WAIT_CLEAR_APPROVAL = range(4)

# Chat_data keys
DK_JOBS = 'jobs'
DK_CURJOB = 'curjob'
DK_TIMES = 'times'
DK_STATISTICS = 'statistics'
DK_TOTALJOBTIME = 'total_job_time'
DK_TOTALPAUSETIME = 'total_pause_time'
DK_NUMBERPAUSES = 'number_of_pauses'

# Commands
CMD_START = 'start'
CMD_PAUSE = 'pause'
CMD_STOP = 'stop'
CMD_RESUME = 'resume'
CMD_LIST = 'list'
CMD_CLEAR = 'clear'
CMD_HELP = 'help'

# Reply messages
MSGC_WELCOME = "Hi! I can track your time. Just use buttons to manage or use /help to get more information"
MSGC_JOBSTARTED = 'Started on {}'
MSGC_JOBALREADYRUNNING = 'The track is already running. Time: {} / {}'
MSGC_JOBPAUSED = 'Paused. Time: {} / {}'
MSGC_JOBALREADYPAUSED = 'The track was already paused. Time: {} / {}'
MSGC_JOBALREADYSTOPPEDFORPAUSE = 'No running track to pause. Start new track with /start command'
MSGC_JOBRESUMED = 'Resumed. Time: {} / {}'
MSGC_JOBSTOPPED = 'Stopped.\nTotal work time: {} with {} pauses for {}.'
MSGC_JOBALREADYSTOPPED = 'No active track. Use /start to start new track or /list to check your previous tracks.'
MSGC_LSNOTRACKSYET = 'You have no tracks yet. Use /start command to start recording one'
MSGC_CLEARWARNING = 'You have {} recorded tracks. If you really want to delete all of them, please send me \'yes\'. Send \'no\' if you have changed your mind'
MSGC_CLEARNODATA = 'You have no recorded tracks. You can start new track with /start command'
MSGC_CLEARSUCCESS = 'All your track are successfully cleared. You can start new track with /start command.'
MSGC_CLEARABORT = 'Your tracks are NOT cleared!'

MSGC_HELP = '/start - starts new track (or resumes paused track)'+\
			'\n/pause - pauses current track'+\
			'\n/resume - resumes current track (or starts new one if current was stopped)'+\
			'\n/stop - stops current track'+\
			'\n/list - lists all the recorded tracks'+\
			'\n/clear - clears all the recorded tracks (requires confirmation)'+\
			'\n/help - shows this message'