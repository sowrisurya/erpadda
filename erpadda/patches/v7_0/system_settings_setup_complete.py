from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype('System Settings')
	companies = vmraid.db.sql("""select name, country
		from tabCompany order by creation asc""", as_dict=True)
	if companies:
		vmraid.db.set_value('System Settings', 'System Settings', 'setup_complete', 1)

	for company in companies:
		if company.country:
			vmraid.db.set_value('System Settings', 'System Settings', 'country', company.country)
			break


