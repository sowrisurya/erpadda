# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
from vmraid import _

def get_data():
	return {
		'fieldname': 'assessment_group',
		'transactions': [
			{
				'label': _('Assessment'),
				'items': ['Assessment Plan', 'Assessment Result']
			}
		]
	}