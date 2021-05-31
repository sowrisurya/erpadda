# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	doctype = 'POS Profile'
	vmraid.reload_doctype(doctype)

	for pos in vmraid.get_all(doctype, filters={'disabled': 0}):
		doc = vmraid.get_doc(doctype, pos.name)

		if not doc.user: continue

		try:
			pos_profile_name = doc.user + ' - ' + doc.company
			doc.flags.ignore_validate  = True
			doc.flags.ignore_mandatory = True
			doc.save()

			vmraid.rename_doc(doctype, doc.name, pos_profile_name, force=True)
		except vmraid.LinkValidationError:
			vmraid.db.set_value("POS Profile", doc.name, 'disabled', 1)
