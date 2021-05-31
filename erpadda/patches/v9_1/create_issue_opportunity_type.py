# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _

def execute():
	# delete custom field if exists
	for doctype, fieldname in (('Issue', 'issue_type'), ('Opportunity', 'opportunity_type')):
		custom_field = vmraid.db.get_value("Custom Field", {"fieldname": fieldname, 'dt': doctype})
		if custom_field:
			vmraid.delete_doc("Custom Field", custom_field, ignore_permissions=True)

	vmraid.reload_doc('support', 'doctype', 'issue_type')
	vmraid.reload_doc('support', 'doctype', 'issue')
	vmraid.reload_doc('crm', 'doctype', 'opportunity_type')
	vmraid.reload_doc('crm', 'doctype', 'opportunity')

	# rename enquiry_type -> opportunity_type
	from vmraid.model.utils.rename_field import rename_field
	rename_field('Opportunity', 'enquiry_type', 'opportunity_type')

	# create values if already set
	for opts in (('Issue', 'issue_type', 'Issue Type'),
		('Opportunity', 'opportunity_type', 'Opportunity Type')):
		for d in vmraid.db.sql('select distinct {0} from `tab{1}`'.format(opts[1], opts[0])):
			if d[0] and not vmraid.db.exists(opts[2], d[0]):
				vmraid.get_doc(dict(doctype = opts[2], name=d[0])).insert()

	# fixtures
	for name in ('Hub', _('Sales'), _('Support'), _('Maintenance')):
		if not vmraid.db.exists('Opportunity Type', name):
			vmraid.get_doc(dict(doctype = 'Opportunity Type', name=name)).insert()
