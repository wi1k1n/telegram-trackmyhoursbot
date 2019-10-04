import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)


class DBHandler(object):
	""" Handles workflow that involves communication with database """
	def __init__(self, path):
		self.path = path

	def create_table_tasks(self):
		self._execute_query(""" CREATE TABLE IF NOT EXISTS tasks (
									uid integer PRIMARY KEY,
									chat_id integer NOT NULL,
									start_datetime INTEGER,
									end_datetime INTEGER,
									label string
								); """)

	def get_task_list(self, chat_id):
		cursor = self._execute_query("SELECT * FROM tasks WHERE 'chat_id' = ?", (chat_id, ))
		pass

	def create_task(self, chat_id):
		cursor = self._execute_query("INSERT")

	def _create_connection(self):
		con = None
		try:
			con = sqlite3.connect(self.path)
		except Error as e:
			logger.error(e)
		return con

	def _execute_query(self, query, values=None):
		con = self._create_connection()
		with con:
			try:
				c = con.cursor()
				if values is None:
					c.execute(query)
				else:
					c.execute(query, values)
			except Error as e:
				logger.error(e)
			return c