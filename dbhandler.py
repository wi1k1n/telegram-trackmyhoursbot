from peewee import *
import logging, datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('main.db')

class BaseModel(Model):
	class Meta:
		database = db

class Task(BaseModel):
	chat_id = IntegerField()
	label = CharField(null=True)
	start = DateField()
	end = DateField(null=True)

db.create_tables([Task])

def get_tasks_list(chat_id):
	return Task.select().where(Task.chat_id == chat_id)

# Creates task and returns 1 if task created successfully
def create_task(chat_id, start=None, end=None, label=''):
	if start is None: start = int(datetime.datetime.timestamp(datetime.datetime.now()))
	t = Task(chat_id=chat_id, start=start, end=end, label=label)
	return t.save()