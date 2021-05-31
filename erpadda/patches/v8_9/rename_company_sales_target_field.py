from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import rename_field

def execute():
	vmraid.reload_doc("setup", "doctype", "company")
	if vmraid.db.has_column('Company', 'sales_target'):
		rename_field("Company", "sales_target", "monthly_sales_target")
