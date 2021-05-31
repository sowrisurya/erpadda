from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname':  'leave_policy',
		'transactions': [
			{
				'label': _('Leaves'),
				'items': ['Leave Allocation']
			},
		]
	}