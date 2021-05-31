# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	""" delete deprecated reports """

	reports = [
		"Monthly Salary Register", "Customer Addresses And Contacts",
		"Supplier Addresses And Contacts"
	]

	for report in reports:
		if vmraid.db.exists("Report", report):
			check_and_update_auto_email_report(report)
			vmraid.db.commit()

			vmraid.delete_doc("Report", report, ignore_permissions=True)

def check_and_update_auto_email_report(report):
	""" delete or update auto email report for deprecated report """

	auto_email_report = vmraid.db.get_value("Auto Email Report", {"report": report})
	if not auto_email_report:
		return

	if report == "Monthly Salary Register":
		vmraid.delete_doc("Auto Email Report", auto_email_report)

	elif report in ["Customer Addresses And Contacts", "Supplier Addresses And Contacts"]:
		vmraid.db.set_value("Auto Email Report", auto_email_report, "report", report)