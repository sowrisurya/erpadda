from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'therapy_session',
		'transactions': [
			{
				'label': _('Assessments'),
				'items': ['Patient Assessment']
			}
		]
	}
