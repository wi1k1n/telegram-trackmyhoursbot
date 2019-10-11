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




# def list(update, context):
# 	chat_id = update.message.chat_id
# 	tasks = dbh.get_tasks_list(chat_id)
#
# 	reply_msg = 'You have {0} timers:'.format(len(tasks))
# 	for task in tasks:
# 		reply_msg += '\n{0}: {1} -> {2}'.format('Unlabeled' if len(task.label) == 0 else task.label,
# 												task.start,
# 												'Now' if task.end is None else task.end)
# 	update.message.reply_text(reply_msg)
#
# def new(update, context):
# 	# update.message.reply_text("WARNING: Function 'new' is not implemented yet!")
#
# 	task = dbh.create_task(update.message.chat_id)
#
# 	reply_msg = 'You have created a timer starting at {0}.\n' \
# 				'You can label this timer, pick a category or set the time of end'.format(task.start)
# 	keyboard = create_keyboard([[('Label', '/label'), ('Category', '/category'), ('Set end', '/end')],
# 								[('Start new timer', '/new'), ('List timers', '/list'), ('Add manually', '/add')]])
# 	update.message.reply_text(reply_msg, reply_markup=ikbmkp(keyboard))
#
# def pause(update, context):
# 	update.message.reply_text("WARNING: Function 'pause' is not implemented yet!")
#
# def resume(update, context):
# 	update.message.reply_text("WARNING: Function 'resume' is not implemented yet!")
#
# def stop(update, context):
# 	update.message.reply_text("WARNING: Function 'stop' is not implemented yet!")
#
# def add(update, context):
# 	update.message.reply_text("WARNING: Function 'add' is not implemented yet!")
#
# def destroy(update, context):
# 	update.message.reply_text("WARNING: Function 'destroy' is not implemented yet!")
#
# def about(update, context):
# 	update.message.reply_text("WARNING: Function 'about' is not implemented yet!")
#
#
# def button(update, context):
# 	query = update.callback_query
#
# 	query.edit_message_text(text="Selected option: {}".format(query.data))
