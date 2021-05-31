from __future__ import unicode_literals
import vmraid

def execute():
	if not vmraid.db.exists("Party Type", "Member"):
		vmraid.reload_doc("non_profit", "doctype", "member")
		party = vmraid.new_doc("Party Type")
		party.party_type = "Member"
		party.save()
