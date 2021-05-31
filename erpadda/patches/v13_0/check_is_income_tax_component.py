# Copyright (c) 2019, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid, erpadda
from erpadda.regional.india.setup import setup

def execute():

	doctypes = ['salary_component',
		'Employee Tax Exemption Declaration',
		'Employee Tax Exemption Proof Submission',
		'Employee Tax Exemption Declaration Category',
		'Employee Tax Exemption Proof Submission Detail',
		'gratuity_rule',
		'gratuity_rule_slab',
		'gratuity_applicable_component'
	]

	for doctype in doctypes:
		vmraid.reload_doc('Payroll', 'doctype', doctype)


	reports = ['Professional Tax Deductions', 'Provident Fund Deductions']
	for report in reports:
		vmraid.reload_doc('Regional', 'Report', report)
		vmraid.reload_doc('Regional', 'Report', report)

	if erpadda.get_region() == "India":
		setup(patch=True)

	if vmraid.db.exists("Salary Component", "Income Tax"):
		vmraid.db.set_value("Salary Component", "Income Tax", "is_income_tax_component", 1)
	if vmraid.db.exists("Salary Component", "TDS"):
		vmraid.db.set_value("Salary Component", "TDS", "is_income_tax_component", 1)

	components = vmraid.db.sql("select name from `tabSalary Component` where variable_based_on_taxable_salary = 1", as_dict=1)
	for component in components:
		vmraid.db.set_value("Salary Component", component.name, "is_income_tax_component", 1)

	if erpadda.get_region() == "India":
		if vmraid.db.exists("Salary Component", "Provident Fund"):
			vmraid.db.set_value("Salary Component", "Provident Fund", "component_type", "Provident Fund")
		if vmraid.db.exists("Salary Component", "Professional Tax"):
			vmraid.db.set_value("Salary Component", "Professional Tax", "component_type", "Professional Tax")