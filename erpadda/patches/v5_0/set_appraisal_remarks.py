# Copyright (c) 2013, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Appraisal")
	vmraid.db.sql("update `tabAppraisal` set remarks = comments")