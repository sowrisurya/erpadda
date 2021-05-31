# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('manufacturing', 'doctype', 'bom_operation')
	for d in vmraid.db.sql("""select name from `tabBOM` where docstatus < 2""", as_dict=1):
		try:
			bom = vmraid.get_doc('BOM', d.name)
			bom.flags.ignore_validate_update_after_submit = True
			bom.calculate_cost()
			bom.save()
			vmraid.db.commit()
		except:
			vmraid.db.rollback()
