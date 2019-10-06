from dbhandler import DBHandler

dbh = DBHandler('main.db')
dbh.create_table_tasks()

tasks = dbh.get_task_list(278720684)
if tasks is None: print('Get tasks list command failed')
else:
	print('You have {0} tasks.'.format(len(tasks)))
	for task in tasks:
		print(task)