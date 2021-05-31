from __future__ import unicode_literals
import vmraid

def execute():
	for project in vmraid.db.sql_list("select name from tabProject"):
		vmraid.reload_doc("projects", "doctype", "project")
		p = vmraid.get_doc("Project", project)
		p.update_milestones_completed()
		p.db_set("percent_milestones_completed", p.percent_milestones_completed)
