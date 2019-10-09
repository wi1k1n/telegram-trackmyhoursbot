import dbhandler as dbh

r = dbh.delete_chat(20)
# dbh.create_chat(20)

dbh.create_chat(10)
dbh.create_chat(20)
tasks = dbh.get_tasks_list(10)
dbh.create_task(10)
tasks = dbh.get_tasks_list(10)
dbh.create_task(10)
tasks = dbh.get_tasks_list(10)
dbh.create_task(10)
dbh.create_task(20)
tasks = dbh.get_tasks_list(10)
tasks = dbh.get_tasks_list(20)
if tasks is None: print('Get tasks list command failed')
else:
	print('You have {0} tasks.'.format(len(tasks)))
	for task in tasks:
		print(task)