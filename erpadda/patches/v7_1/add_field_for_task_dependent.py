from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Task')
	for t in vmraid.get_all('Task', fields=['name']):
		task = vmraid.get_doc('Task', t.name)
		task.update_depends_on()
		if task.depends_on_tasks:
			task.db_set('depends_on_tasks', task.depends_on_tasks, update_modified=False)
