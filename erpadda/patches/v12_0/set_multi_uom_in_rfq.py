# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import flt
from erpadda.stock.get_item_details import get_conversion_factor

def execute():
	vmraid.reload_doc('buying', 'doctype', 'request_for_quotation_item')

	vmraid.db.sql("""UPDATE `tabRequest for Quotation Item`
			SET
				stock_uom = uom,
				conversion_factor = 1,
				stock_qty = qty""")