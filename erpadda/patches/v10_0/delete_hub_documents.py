from __future__ import unicode_literals

import vmraid
from vmraid.model.utils.rename_field import rename_field

def execute():
	for dt, dn in (("Page", "Hub"), ("DocType", "Hub Settings"), ("DocType", "Hub Category")):
		vmraid.delete_doc(dt, dn, ignore_missing=True)

	if vmraid.db.exists("DocType", "Data Migration Plan"):
		data_migration_plans = vmraid.get_all("Data Migration Plan", filters={"module": 'Hub Node'})
		for plan in data_migration_plans:
			plan_doc = vmraid.get_doc("Data Migration Plan", plan.name)
			for m in plan_doc.get("mappings"):
				vmraid.delete_doc("Data Migration Mapping", m.mapping, force=True)
			docs = vmraid.get_all("Data Migration Run", filters={"data_migration_plan": plan.name})
			for doc in docs:
				vmraid.delete_doc("Data Migration Run", doc.name)
			vmraid.delete_doc("Data Migration Plan", plan.name)
