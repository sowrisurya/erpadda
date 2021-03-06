import vmraid
from erpadda.regional.india.setup import make_custom_fields

def execute():
	if vmraid.get_all('Company', filters = {'country': 'India'}):
		make_custom_fields()

		if not vmraid.db.exists('Party Type', 'Donor'):
			vmraid.get_doc({
				'doctype': 'Party Type',
				'party_type': 'Donor',
				'account_type': 'Receivable'
			}).insert(ignore_permissions=True)
