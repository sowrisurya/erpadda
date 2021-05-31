# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if not vmraid.db.exists({"doctype": "Assessment Group","assessment_group_name": "All Assessment Groups"}):
		vmraid.reload_doc("education", "doctype", "assessment_group")
		doc = vmraid.new_doc("Assessment Group")
		doc.assessment_group_name = "All Assessment Groups"
		doc.is_group = 1
		doc.flags.ignore_mandatory = True
		doc.save()