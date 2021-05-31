# Copyright (c) 2013, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('crm', 'doctype', 'opportunity')
	vmraid.reload_doc('crm', 'doctype', 'opportunity_item')

	# all existing opportunities were with items
	vmraid.db.sql("update `tabDocType` set module = 'CRM' where name='Opportunity Item'")
	vmraid.db.sql("update tabOpportunity set with_items=1, title=customer_name")
	vmraid.db.sql("update `tabEmail Account` set append_to='Opportunity' where append_to='Lead'")
