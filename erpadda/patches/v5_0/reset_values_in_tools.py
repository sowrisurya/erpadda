# Copyright (c) 2013, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	for dt in ["Payment Tool", "Bank Reconciliation", "Payment Reconciliation", "Leave Control Panel", 
		"Salary Manager", "Upload Attenadance", "Production Planning Tool", "BOM Update Tool", "Customize Form",
		 "Employee Attendance Tool", "Rename Tool", "BOM Update Tool", "Process Payroll", "Naming Series"]:
			vmraid.db.sql("delete from `tabSingles` where doctype=%s", dt)
		