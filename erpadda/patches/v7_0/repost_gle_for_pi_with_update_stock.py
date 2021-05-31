# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import cint

def execute():
	vmraid.reload_doctype("Purchase Invoice")

	for pi in vmraid.db.sql("""select name from `tabPurchase Invoice`
		where company in(select name from tabCompany where enable_perpetual_inventory = 1) and
		update_stock=1 and docstatus=1 order by posting_date asc""", as_dict=1):

			vmraid.db.sql("""delete from `tabGL Entry`
				where voucher_type = 'Purchase Invoice' and voucher_no = %s""", pi.name)

			pi_doc = vmraid.get_doc("Purchase Invoice", pi.name)
			pi_doc.make_gl_entries()
			vmraid.db.commit()