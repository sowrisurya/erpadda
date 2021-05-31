from __future__ import unicode_literals
import vmraid

def execute():
	if not vmraid.db.exists("Role", "Stock User"):
		vmraid.rename_doc("Role", "Material User", "Stock User")
	if not vmraid.db.exists("Role", "Stock Manager"):
		vmraid.rename_doc("Role", "Material Manager", "Stock Manager")
	if not vmraid.db.exists("Role", "Item Manager"):
		vmraid.rename_doc("Role", "Material Master Manager", "Item Manager")
