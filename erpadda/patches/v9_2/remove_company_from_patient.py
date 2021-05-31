from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("DocType", "Patient"):
		if 'company' in vmraid.db.get_table_columns("Patient"):
			vmraid.db.sql("alter table `tabPatient` drop column company")
