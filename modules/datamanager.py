import os, os.path as op
import pickle
from modules.user import User

class DataManager:
	def __init__(self, path=None):
		self.db = None
		self.path = 'data/main.db'

		if path:
			self.path = path
		self.initialize()

	def __getitem__(self, id):
		return self.db[id]

	def addUser(self, usr):
		if not self.hasUser(usr):
			self.db[usr.id] = User(usr)

	def hasUser(self, usr):
		return usr.id in self.db

	def initialize(self, dontCreate=False):
		""" Load database or create if not exists """
		if not dontCreate:
			os.makedirs(op.dirname(self.path), exist_ok=True)

		self.db = dict()
		if op.isfile(self.path):
			self.load()
		elif not dontCreate:
			self.save()

	def load(self):
		if op.isfile(self.path):
			with open(self.path, 'rb') as f:
				self.db = pickle.load(f)

	def save(self):
		with open(self.path, 'wb') as f:
			pickle.dump(self.db, f)