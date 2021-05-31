from __future__ import unicode_literals
import vmraid
from erpadda.regional.india import states

def execute():
	company = vmraid.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	if not vmraid.db.get_value("Custom Field", filters={'fieldname':'gst_state'}):
		return

	vmraid.db.sql("update `tabCustom Field` set options=%s where fieldname='gst_state'", '\n'.join(states))
	vmraid.db.sql("update `tabAddress` set gst_state='Chhattisgarh' where gst_state='Chattisgarh'")
	vmraid.db.sql("update `tabAddress` set gst_state_number='05' where gst_state='Uttarakhand'")
