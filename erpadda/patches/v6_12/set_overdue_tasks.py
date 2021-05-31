from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Task")

	from erpadda.projects.doctype.task.task import set_tasks_as_overdue
	set_tasks_as_overdue()
