import datetime as dt

def inann(dict, key):
	""" Takes dictionary and key and checks if key in dictionary and it is not None """
	return key in dict and not dict[key] is None

def ninann(dict, key):
	""" Takes dictionary and key and checks if key not in dictionary or it is None """
	return not key in dict or dict[key] is None

def curTimeStamp():
	""" Returns current timestamp """
	return dt.datetime.now().timestamp()

def formatTimeStamp(ts, mode='full'):
	"""
	Takes timestamp and returna human-readable formatted version
	:param mode: can be 'full' for date+time format, 'date' for only date and 'time' for only time
	"""
	dtime = dt.datetime.fromtimestamp(ts)
	if mode == 'full':
		return dtime.strftime('%d/%m/%Y %H:%M:%S')
	elif mode == 'date':
		return dtime.strftime('%d/%m/%Y')
	elif mode == 'time':
		return dtime.strftime('%H:%M:%S')

def formatSeconds(seconds):
	""" Takes seconds (float) and returns formated string with days/hours/minutes/seconds """
	if seconds == 0: return '0s'
	td = dt.timedelta(seconds=seconds)
	days = td.days
	hours = td.seconds//3600
	minutes = td.seconds%3600//60
	seconds = td.seconds%60
	ret = ''
	startedFlag = False
	if startedFlag or days > 0:
		ret += '{}d'.format(days)
		startedFlag = True
	if startedFlag or hours > 0:
		ret += ' {}h'.format(hours)
		startedFlag = True
	if startedFlag or minutes > 0:
		ret += ' {}m'.format(minutes)
		startedFlag = True
	if startedFlag or seconds > 0:
		ret += ' {}s'.format(seconds)
	return ret.strip()