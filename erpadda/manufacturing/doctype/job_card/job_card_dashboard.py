from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'job_card',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Material Request', 'Stock Entry']
			}
		]
	}
