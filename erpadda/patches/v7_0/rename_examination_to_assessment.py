# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

from vmraid.model.utils.rename_field import rename_field

def execute():
	if vmraid.db.exists("DocType", "Examination"):
		vmraid.rename_doc("DocType", "Examination", "Assessment")
		vmraid.rename_doc("DocType", "Examination Result", "Assessment Result")

		# 'Schools' module changed to the 'Education'
		# vmraid.reload_doc("schools", "doctype", "assessment")
		# vmraid.reload_doc("schools", "doctype", "assessment_result")

		vmraid.reload_doc("education", "doctype", "assessment")
		vmraid.reload_doc("education", "doctype", "assessment_result")

		rename_field("Assessment", "exam_name", "assessment_name")
		rename_field("Assessment", "exam_code", "assessment_code")
	
		vmraid.db.sql("delete from `tabPortal Menu Item` where route = '/examination'")