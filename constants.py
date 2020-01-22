# States for ConversationHangler
STATE_WAIT_FOR_START, \
STATE_RUNNING, \
STATE_PAUSED = range(3)

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

# Reply messages
MSGC_WELCOME = "Hi! I can track your time. Just use buttons to manage or use /help to get more information"
MSGC_JOBSTARTED = 'Started on {}'
MSGC_JOBPAUSED = 'Paused at {}'
MSGC_JOBRESUMED = 'Resumed at {}'
MSGC_JOBSTOPPED = 'Stopped on {}\nTotal time: {}{}'
MSGC_JOBSTOPPED_PAUSESEXTRA = '\nTotal pause time: {} ({} {})'
MSGC_JOBSTOPPED_WITHOUTPAUSES = '\nTotal working time: {}'
