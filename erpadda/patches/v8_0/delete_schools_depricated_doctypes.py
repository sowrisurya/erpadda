# Copyright (c) 2017, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	""" delete doctypes """

	if vmraid.db.exists("DocType", "Grading Structure"):
		vmraid.delete_doc("DocType", "Grading Structure", force=1)

	if vmraid.db.exists("DocType", "Grade Interval"):
		vmraid.delete_doc("DocType", "Grade Interval", force=1)