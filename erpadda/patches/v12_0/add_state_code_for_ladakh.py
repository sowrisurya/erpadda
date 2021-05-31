import vmraid
from erpadda.regional.india import states

def execute():

	company = vmraid.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	custom_fields = ['Address-gst_state', 'Tax Category-gst_state']

	# Update options in gst_state custom fields
	for field in custom_fields:
		if vmraid.db.exists('Custom Field', field):
			gst_state_field = vmraid.get_doc('Custom Field', field)
			gst_state_field.options = '\n'.join(states)
			gst_state_field.save()
