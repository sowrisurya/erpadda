from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'appointment_type',
		'transactions': [
			{
				'label': _('Patient Appointments'),
				'items': ['Patient Appointment']
			},
		]
	}
