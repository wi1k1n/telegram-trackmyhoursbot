from peewee import *
import logging, datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

db = SqliteDatabase('main.db')

class BaseModel(Model):
	class Meta:
		database = db

class Chat(BaseModel):
	chat_id = IntegerField()

class Task(BaseModel):
	chat_id = ForeignKeyField(Chat, backref='tasks')
	label = CharField(null=True)
	start = DateField()
	end = DateField(null=True)

db.create_tables([Chat, Task])

def get_tasks_list(chat_id):
	return Task.select().join(Chat).where(Chat.chat_id == chat_id)

# Checks chat_id for existence and returns 1 if exists, 0 - if not exists, other - error
def chat_exists(chat_id):
	chats = Chat.select().where(Chat.chat_id == chat_id)
	if len(chats) == 1:
		return 1
	elif len(chats) > 1:
		logger.warning('{1} duplicates for chat_id=\'{0}\' exists!'.format(chat_id, len(chats) - 1))
		return len(chats)
	return 0

# Creates new chat entry and returns 1 if created successfully, 0 - if already exists, other - error
def create_chat(chat_id):
	chats = Chat.select().where(Chat.chat_id == chat_id)
	if len(chats) == 0:
		return Chat(chat_id=chat_id).save()
	elif len(chats) > 1:
		logger.warning('{1} duplicates for chat_id=\'{0}\' exists! New entry has not been created'.format(chat_id, len(chats) - 1))
		return len(chats)
	return 0

# Deletes chat entry and returns 1 if deletes successfully, 0 - if no chat found, other - error
def delete_chat(chat_id):
	chats = Chat.select().where(Chat.chat_id == chat_id)
	if len(chats) == 1:
		return chats.get().delete_instance()
	elif len(chats) > 1:
		logger.warning('{1} duplicates for chat_id=\'{0}\' exists! Entry has not been deleted'.format(chat_id, len(chats) - 1))
		return len(chats)
	return 0

# Creates task and returns 1 if created successfully
def create_task(chat_id, start=None, end=None, label=''):
	# TODO: check for label duplicate
	if start is None: start = int(datetime.datetime.timestamp(datetime.datetime.now()))
	t = Task(chat_id=chat_id, start=start, end=end, label=label)
	return t.save()