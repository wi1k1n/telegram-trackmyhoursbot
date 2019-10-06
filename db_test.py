import dbhandler as dbh

# dbh.create_task(12)
tasks = dbh.get_tasks_list(12)
if tasks is None: print('Get tasks list command failed')
else:
	print('You have {0} tasks.'.format(len(tasks)))
	for task in tasks:
		print(task)