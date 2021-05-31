from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'work_order',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Stock Entry', 'Job Card', 'Pick List']
			}
		]
	}