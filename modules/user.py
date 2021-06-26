from enum import Enum
from util import *
import numpy as np

class State(Enum):
	STOPPED = 0
	RUNNING = 1
	PAUSED = 2

class User:
	def __init__(self, usr):
		self.id = usr.id
		self.firstName = usr.first_name
		self.lastName = usr.last_name if hasattr(usr, 'last_name') else ''
		self.username = usr.username if hasattr(usr, 'username') else ''
		self.language = usr.language_code if hasattr(usr, 'language_code') else ''

		self.blocked = usr.is_bot
		self.state = State.STOPPED
		self.intervals = []

	def startTimer(self, ts=None):
		""" Resumes if paused, starts new if stopped, does nothing if running """
		if ts is None:
			ts = curTimeStamp()
		if self.state == State.PAUSED:
			if not len(self.intervals):
				self.intervals.append([ts])
			else:
				self.intervals[-1].append(ts)
		elif self.state == State.STOPPED:
			self.intervals.append([ts])
		self.state = State.RUNNING
		return ts

	def pauseTimer(self, ts=None):
		if ts is None:
			ts = curTimeStamp()
		if self.state == State.RUNNING:
			if len(self.intervals):
				self.intervals[-1].append(ts)
			self.state = State.PAUSED
		return ts

	def stopTimer(self, ts=None):
		if ts is None:
			ts = curTimeStamp()
		if self.state == State.RUNNING:
			if len(self.intervals):
				self.intervals[-1].append(ts)
		self.state = State.STOPPED
		return ts

	def getIntervalStat(self, idx):
		if idx >= len(self.intervals) or idx < -len(self.intervals) or not len(self.intervals[idx]):
			return (None, None, None, None, None)
		interval = self.intervals[idx]
		tsStart = interval[0]
		running = len(interval) % 2
		int4work = np.array(interval)
		if running:
			int4work = np.concatenate((int4work, [curTimeStamp()]))
		timeWork = sum(int4work[1::2]) - sum(int4work[0::2])
		int4Pause = int4work[1:-1]
		timePause = sum(int4Pause[1::2]) - sum(int4Pause[0::2])
		return (tsStart, timeWork, timePause, (len(int4work)-1) - len(int4work)//2, running)