from peewee import *
import logging, datetime
import bits

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

class DBHandler(object):
	class BaseModel(Model):
		class Meta:
			database = db
	""" Handles workflow that involves communication with database """
	def __init__(self, path):
		self.path = path
		self.db = SqliteDatabase(self.path)

	def create_table_tasks(self):
		self.connect()
		self.execute(""" CREATE TABLE IF NOT EXISTS tasks (
									uid integer PRIMARY KEY,
									chat_id integer NOT NULL,
									start_datetime INTEGER,
									end_datetime INTEGER,
									label string
								); """)
		self.close()
		return self.error() is None

	def get_task_list(self, chat_id):
		self.connect()
		self.execute('SELECT * FROM tasks WHERE chat_id = {chat_id}'.format(chat_id=chat_id))
		tasks = self.cursor.fetchall()
		self.close()
		if self.error() is not None:
			return None
		return tasks

	def create_task(self, chat_id, start=None, end=None, label=None):
		if start is None: start = int(datetime.datetime.timestamp(datetime.datetime.now()))
		cols = '(chat_id, start_datetime'
		qms = '(?, ?'
		values = (chat_id, start)
		if end is not None:
			cols += ', end_datetime'
			qms += ', ?'
			values += (end, )
		if label is not None:
			cols += ', label'
			qms += ', ?'
			values += (label, )
		cols += ')'
		qms += ')'
		self.connect()
		self.execute("INSERT INTO tasks {cols} VALUES {qms}".format(cols=cols, qms=qms), values)
		self.close()
		return self.error() is None

	# Connects to database
	def connect(self):
		self.con = None
		self.error_code = 0
		try:
			self.con = sqlite3.connect(self.path)
		except Error as e:
			logger.error('Connection to database could not be created. Error: {0}'.format(e))
			self.error_code = bits.setBit(self.error_code, 0)
	def execute(self, query, values=None):
		if self.con is None:
			logger.error('self.con is None. The query has not been executed!')
			self.error_code = bits.setBit(self.error_code, 1)
		try:
			self.cursor = self.con.cursor()
			if values: self.cursor.execute(query, values)
			else: self.cursor.execute(query)
		except Error as e:
			logger.error('Query \'{0}\' with values \'{1}\' could not be executed. Error: {2}'.format(query, values, e))
			self.error_code = bits.setBit(self.error_code, 2)
	def close(self):
		if self.con is None:
			logger.error('self.con is None. The connection cannot be closed!')
			self.error_code = bits.setBit(self.error_code, 3)
		try:
			self.con.commit()
			self.con.close()
		except Error as e:
			logger.error('Connection to database could not be closed. Error: {0}'.format(e))
			self.error_code = bits.setBit(self.error_code, 4)

	def error(self):
		if self.error_code == 0:
			return None
		ret = []
		if bits.testBit(self.error_code, 0): ret.append((0, 'Connection failed'))
		if bits.testBit(self.error_code, 1): ret.append((1, 'No connection for execute command'))
		if bits.testBit(self.error_code, 2): ret.append((2, 'Execute query command failed'))
		if bits.testBit(self.error_code, 3): ret.append((3, 'No connection for close command'))
		if bits.testBit(self.error_code, 4): ret.append((4, 'Close connection command failed'))
		return ret