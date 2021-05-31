# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	company = vmraid.get_all('Company', filters = {'country': 'India'})

	if company:
		for doctype in ['Sales Invoice', 'Delivery Note']:
			vmraid.db.sql(""" update `tab{0}`
				set billing_address_gstin = (select gstin from `tabAddress` 
					where name = customer_address) 
			where customer_address is not null and customer_address != ''""".format(doctype))