# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	doctypes = ["Opportunity", "Quotation", "Sales Order", "Sales Invoice", "Purchase Invoice", "Purchase Order", "Delivery Note", "Purchase Receipt"]
	for doctype in doctypes:
		vmraid.db.sql(""" update `tab{doctype}` set status = 'Draft'
			where status = 'Cancelled' and docstatus = 0 """.format(doctype = doctype))