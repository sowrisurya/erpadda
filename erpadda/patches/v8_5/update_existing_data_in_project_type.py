# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("projects", "doctype", "project_type")
	vmraid.reload_doc("projects", "doctype", "project")

	project_types = ["Internal", "External", "Other"]

	for project_type in project_types:
		if not vmraid.db.exists("Project Type", project_type):
			p_type = vmraid.get_doc({
				"doctype": "Project Type",
				"project_type": project_type
			})
			p_type.insert()