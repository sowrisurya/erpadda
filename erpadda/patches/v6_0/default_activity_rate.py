from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("projects", "doctype", "activity_cost")

	for cost in vmraid.db.get_list("Activity Cost", filters = {"employee": ""},
		fields = ("name", "activity_type", "costing_rate", "billing_rate")):
		activity_type = vmraid.get_doc("Activity Type", cost.activity_type)
		activity_type.costing_rate = cost.costing_rate
		activity_type.billing_rate = cost.billing_rate
		activity_type.save()

		vmraid.delete_doc("Activity Cost", cost.name)
