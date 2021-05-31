# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('accounts', 'doctype', 'purchase_invoice_item')
	vmraid.db.sql("update `tabPurchase Invoice Item` set stock_qty = qty, stock_uom = uom")