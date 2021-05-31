from __future__ import unicode_literals
import vmraid

def execute():
	if not vmraid.db.exists("Party Type", "Student"):
		party = vmraid.new_doc("Party Type")
		party.party_type = "Student"
		party.save()
