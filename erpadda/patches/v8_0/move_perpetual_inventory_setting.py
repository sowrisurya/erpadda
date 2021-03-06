# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('Company')
	enabled = vmraid.db.get_single_value("Accounts Settings", "auto_accounting_for_stock") or 0
	for data in vmraid.get_all('Company', fields = ["name"]):
		doc = vmraid.get_doc('Company', data.name)
		doc.enable_perpetual_inventory = enabled
		doc.db_update()