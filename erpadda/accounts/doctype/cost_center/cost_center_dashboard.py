from __future__ import unicode_literals

from vmraid import _


def get_data():
	return {
		'fieldname': 'cost_center',
		'reports': [
			{
				'label': _('Reports'),
				'items': ['Budget Variance Report', 'General Ledger']
			}
		]
	}