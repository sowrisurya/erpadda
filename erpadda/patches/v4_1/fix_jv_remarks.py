# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	reference_date = guess_reference_date()
	for name in vmraid.db.sql_list("""select name from `tabJournal Entry`
			where date(creation)>=%s""", reference_date):
		jv = vmraid.get_doc("Journal Entry", name)
		try:
			jv.create_remarks()
		except vmraid.MandatoryError:
			pass
		else:
			vmraid.db.set_value("Journal Entry", jv.name, "remark", jv.remark)

def guess_reference_date():
	return (vmraid.db.get_value("Patch Log", {"patch": "erpadda.patches.v4_0.validate_v3_patch"}, "creation")
		or "2014-05-06")
