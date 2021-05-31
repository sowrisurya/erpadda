# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.modules import scrub, get_doctype_module

def execute():
	for dt in ["Quotation", "Sales Order", "Delivery Note", "Sales Invoice"]:
		vmraid.reload_doc(get_doctype_module(dt), "doctype", scrub(dt))
		vmraid.db.sql("""update `tab{0}` set base_discount_amount=discount_amount,
			discount_amount=discount_amount/conversion_rate""".format(dt))
