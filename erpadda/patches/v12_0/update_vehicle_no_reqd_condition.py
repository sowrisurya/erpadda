import vmraid

def execute():
	vmraid.reload_doc('custom', 'doctype', 'custom_field')
	company = vmraid.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	if vmraid.db.exists('Custom Field', { 'fieldname': 'vehicle_no' }):
		vmraid.db.set_value('Custom Field', { 'fieldname': 'vehicle_no' }, 'mandatory_depends_on', '')
