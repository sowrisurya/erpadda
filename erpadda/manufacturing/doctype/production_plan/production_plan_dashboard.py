from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'production_plan',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Work Order', 'Material Request']
			},
		]
	}