from __future__ import unicode_literals

from vmraid import _


def get_data():
	return {
		'fieldname': 'bank',
		'transactions': [
			{
				'label': _('Bank Details'),
				'items': ['Bank Account', 'Bank Guarantee']
			}
		]
	}
