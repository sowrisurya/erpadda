from __future__ import unicode_literals
import vmraid
from vmraid import _

def execute():
	""" assign lft and rgt appropriately """
	if "Healthcare" not in vmraid.get_active_domains():
		return

	vmraid.reload_doc("healthcare", "doctype", "healthcare_service_unit")
	vmraid.reload_doc("healthcare", "doctype", "healthcare_service_unit_type")
	company = vmraid.get_value("Company", {"domain": "Healthcare"}, "name")

	if company:
		vmraid.get_doc({
			'doctype': 'Healthcare Service Unit',
			'healthcare_service_unit_name': _('All Healthcare Service Units'),
			'is_group': 1,
			'company': company
		}).insert(ignore_permissions=True)

