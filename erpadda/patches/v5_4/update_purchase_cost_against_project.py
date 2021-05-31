# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for p in vmraid.get_all("Project"):
		purchase_cost = vmraid.db.sql("""select sum(ifnull(base_net_amount, 0))
			from `tabPurchase Invoice Item` where project = %s and docstatus=1""", p.name)
		purchase_cost = purchase_cost and purchase_cost[0][0] or 0
		
		vmraid.db.set_value("Project", p.name, "total_purchase_cost", purchase_cost)