# Copyright (c) 2019, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from six import iteritems
from erpadda.setup.install import add_non_standard_user_types

def execute():
	doctype_dict = {
		'projects': ['Timesheet'],
		'payroll': ['Salary Slip', 'Employee Tax Exemption Declaration', 'Employee Tax Exemption Proof Submission'],
		'hr': ['Employee', 'Expense Claim', 'Leave Application', 'Attendance Request', 'Compensatory Leave Request']
	}

	for module, doctypes in iteritems(doctype_dict):
		for doctype in doctypes:
			vmraid.reload_doc(module, 'doctype', doctype)


	vmraid.flags.ignore_select_perm = True
	vmraid.flags.update_select_perm_after_migrate = True

	add_non_standard_user_types()