from enum import Enum
from util import *
import numpy as np

class State(Enum):
	STOPPED = 0
	RUNNING = 1
	PAUSED = 2

class Track:
	def __init__(self, ts=None):
		if ts:
			self.intervals = [ts]
			self.state = State.RUNNING
		else:
			self.intervals = []
			self.state = State.STOPPED
		self.noLastWorkInterval = False

	def start(self):
		ts = curTimeStamp()
		if self.state != State.RUNNING:
			self.intervals.append(ts)
		self.state = State.RUNNING
		return ts

	def pause(self):
		ts = curTimeStamp()
		if self.state == State.STOPPED:
			return None
		if self.state == State.RUNNING:
			self.intervals.append(ts)
			self.state = State.PAUSED
		return ts

	def stop(self):
		ts = curTimeStamp()
		if self.state != State.STOPPED:
			self.intervals.append(ts)
			if self.state == State.PAUSED:
				self.noLastWorkInterval = True
		self.state = State.STOPPED
		return ts

	def getStatistics(self):
		if not len(self.intervals):
			return None, 0, 0, 0, 0, 0, 0
		ts = curTimeStamp()
		track = np.array(self.intervals)
		if self.state != State.STOPPED:
			track = np.concatenate((track, [ts]))
		if len(track) % 2:
			t4w = track[:-1]
			t4p = track[1:]
		else:
			t4w = track
			t4p = track[1:-1]
		pn = int(self.noLastWorkInterval)
		# work_time, work_intervals, pause_time, pause_intervals
		return self.intervals[0],\
			   sum(t4w[1::2] - t4w[::2]),\
			   len(track)//2,\
			   sum(t4p[1::2] - t4p[::2]),\
			   (len(t4w)-1)-len(t4w)//2+pn,\
			   self.state


class User:
	def __init__(self, usr):
		self.id = usr.id
		self.firstName = usr.first_name
		self.lastName = usr.last_name if hasattr(usr, 'last_name') else ''
		self.username = usr.username if hasattr(usr, 'username') else ''
		self.language = usr.language_code if hasattr(usr, 'language_code') else ''

		# self.blocked = usr.is_bot
		self.tracks = []


	def startTimer(self):
		""" Resumes if paused, starts new if stopped, does nothing if running """
		if self.state == State.STOPPED:
			self.tracks.append(Track())
		return self.track.start()

	def pauseTimer(self):
		if self.track:
			return self.track.pause()
		return None

	def stopTimer(self):
		return self.track.stop()


	def _getCurTrack(self):
		if len(self.tracks):
			return self.tracks[-1]
		return None
	def _getStateOfCurTrack(self):
		if len(self.tracks):
			return self.track.state
		return State.STOPPED
	def getStatistics(self, ind=-1):
		try:
			return self.tracks[ind].getStatistics()
		except:
			return Track().getStatistics()
	track = property(fget=_getCurTrack)
	state = property(fget=_getStateOfCurTrack)