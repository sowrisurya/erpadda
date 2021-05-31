from __future__ import unicode_literals

from vmraid import _


def get_data():
	return {
		'fieldname': 'task',
		'transactions': [
			{
				'label': _('Activity'),
				'items': ['Timesheet']
			},
			{
				'label': _('Accounting'),
				'items': ['Expense Claim']
			}
		]
	}