# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import vmraid

def execute():
	missing_line = """{{ address_line1 }}<br>"""
	for name, template in vmraid.db.sql("select name, template from `tabAddress Template`"):
		if missing_line not in template:
			d = vmraid.get_doc("Address Template", name)
			d.template = missing_line + d.template
			d.save()
